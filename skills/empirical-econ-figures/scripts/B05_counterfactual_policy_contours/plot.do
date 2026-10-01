version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in fee_change_pct denial_change_pct acceptance_change payment_change_usd {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v')
}
isid fee_change_pct denial_change_pct
egen byte xtag=tag(fee_change_pct)
egen byte ytag=tag(denial_change_pct)
quietly count if xtag
local nx=r(N)
quietly count if ytag
local ny=r(N)
assert `nx'>=5 & `ny'>=5
assert _N==`nx'*`ny'
quietly count if fee_change_pct==0 & denial_change_pct==0 & abs(acceptance_change)<1e-9 & abs(payment_change_usd)<1e-9
assert r(N)==1
quietly summarize acceptance_change
assert r(min)<0 & r(max)>0
quietly summarize payment_change_usd
assert r(min)<-20 & r(max)>20
drop xtag ytag
quietly summarize fee_change_pct
local xmin=r(min)
local xmax=r(max)
quietly summarize denial_change_pct
local ymin=r(min)
local ymax=r(max)
local xstep=(`xmax'-`xmin')/4
local ystep=(`ymax'-`ymin')/6
sort denial_change_pct fee_change_pct
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
mata:
real matrix addsegment(real matrix S, real rowvector p1, real rowvector p2, real scalar styl, real scalar lev)
{
    real rowvector q1,q2
    if (styl==1) {
        S=S\(p1[1],p1[2],4,lev)\(p2[1],p2[2],4,lev)\(.,.,4,lev)
        q1=p1+.43*(p2-p1)
        q2=p1+.57*(p2-p1)
        S=S\(p1[1],p1[2],1,lev)\(q1[1],q1[2],1,lev)\(.,.,1,lev)\(q2[1],q2[2],1,lev)\(p2[1],p2[2],1,lev)\(.,.,1,lev)
    }
    else S=S\(p1[1],p1[2],2,lev)\(p2[1],p2[2],2,lev)\(.,.,2,lev)
    return(S)
}
real matrix segments(real colvector X, real colvector Y, real colvector Z, real scalar nx, real scalar ny, real scalar lev, real scalar styl, real scalar target)
{
    real matrix S, P
    real rowvector ids, xx, yy, zz
    real scalar i, j, e, b, n, t, d, best, bx, by
    S=J(0,4,.)
    best=.
    bx=.
    by=.
    for (j=1;j<ny;j++) {
        for (i=1;i<nx;i++) {
            ids=((j-1)*nx+i, (j-1)*nx+i+1, j*nx+i+1, j*nx+i)
            xx=X[ids]'
            yy=Y[ids]'
            zz=Z[ids]'
            P=J(4,2,.)
            n=0
            for (e=1;e<=4;e++) {
                b=mod(e,4)+1
                if ((zz[e]>=lev)!=(zz[b]>=lev)) {
                    t=(lev-zz[e])/(zz[b]-zz[e])
                    n=n+1
                    P[n,]=(xx[e]+t*(xx[b]-xx[e]), yy[e]+t*(yy[b]-yy[e]))
                }
            }
            if (n==2 | n==4) {
                S=addsegment(S,P[1,],P[2,],styl,lev)
                if (styl==1) {
                    d=abs((P[1,2]+P[2,2])/2-target)
                    if (missing(best) | d<best) {
                        best=d
                        bx=(P[1,1]+P[2,1])/2
                        by=(P[1,2]+P[2,2])/2
                    }
                }
                if (n==4) S=addsegment(S,P[3,],P[4,],styl,lev)
            }
        }
    }
    if (styl==1 & !missing(best)) S=S\(bx,by,3,lev)
    return(S)
}
void make_contours(real scalar nx, real scalar ny)
{
    real colvector X,Y,A,P
    real matrix S
    real scalar lev, oldn
    X=st_data(.,"fee_change_pct")
    Y=st_data(.,"denial_change_pct")
    A=st_data(.,"acceptance_change")
    P=st_data(.,"payment_change_usd")
    S=J(0,4,.)
    for (lev=-20;lev<=20;lev=lev+5) S=S\segments(X,Y,P,nx,ny,lev,1,-20)
    S=S\segments(X,Y,A,nx,ny,0,2,-20)
    oldn=st_nobs()
    st_addvar("double",("plot_x","plot_y","plot_style","contour_level"))
    st_addobs(rows(S))
    st_store((oldn+1::oldn+rows(S)),("plot_x","plot_y","plot_style","contour_level"),S)
}
end
mata: make_contours(`nx',`ny')
format contour_level %9.0f
preserve
keep if !missing(plot_x) & !missing(plot_y)
keep plot_x plot_y plot_style contour_level
export delimited using "`base'_contours.csv", replace
restore
local titleopt ""
if "`lang'"=="zh" {
    local xlab "费用变化（%）"
    local ylab "拒付概率相对变化（%）"
    local accept "接受率不变"
    local pay "每次就诊支付变化（美元）"
    local origin "观测基准"
    if "`showtitle'"=="1" local titleopt `"title("费用与拒付的政策反事实")"'
}
else {
    local xlab "Change in fee (%)"
    local ylab "Relative change in denial probability (%)"
    local accept "Constant acceptance"
    local pay "Payment change ($/visit)"
    local origin "Observed baseline"
    if "`showtitle'"=="1" local titleopt `"title("Policy counterfactuals: fees and denials")"'
}
twoway (line plot_y plot_x if plot_style==1, lcolor(gs7) lpattern(dash) lwidth(medium) cmissing(n)) ///
       (line plot_y plot_x if plot_style==2, lcolor(black) lwidth(thick) cmissing(n)) ///
       (scatter plot_y plot_x if plot_style==3, msymbol(i) mlabel(contour_level) mlabcolor(gs4) mlabsize(small)) ///
       (scatter denial_change_pct fee_change_pct if fee_change_pct==0 & denial_change_pct==0, ///
           mcolor("190 46 60") msize(medium)), ///
       xtitle("`xlab'") ytitle("`ylab'") xscale(range(`xmin' `xmax') noextend) yscale(range(`ymin' `ymax') noextend) ///
       xlabel(`xmin'(`xstep')`xmax',nogrid) ylabel(`ymin'(`ystep')`ymax',angle(horizontal) nogrid) ///
       legend(order(2 "`accept'" 1 "`pay'" 4 "`origin'") position(6) ring(1) rows(1) size(small) region(lcolor(none))) ///
       graphregion(color(white)) plotregion(color(white)) `titleopt'
graph export "`output'", width(1900) replace
graph export "`base'.pdf", replace
