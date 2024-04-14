import pearson3curve as p3
import pearson3curve.plot as p3plot

# 本例取自《工程水文学》（2000年第3版，詹道江 叶守泽 合编）P196表7-3
data = p3.Data(
    [
        1540,
        980,
        1090,
        1050,
        1860,
        1140,
        790,
        2750,
        762,
        2390,
        1210,
        1270,
        1200,
        1740,
        883,
        1260,
        408,
        1050,
        1520,
        483,
        794,
    ]
)

mex, mcv, mcs = p3.get_moments(data)
fex, fcv, fcs = p3.get_fitted_moments(data, moments=(mex, mcv, mcs))

p3plot.scatter(data)
p3plot.plot(p3.Curve(mex, mcv, mcs), label="Unfitted curve", linestyle="--")
p3plot.plot(p3.Curve(fex, fcv, fcs), label="Fitted curve")

p3plot.legend()
p3plot.show()
p3plot.save("example/successive.png", dpi=300, transparent=False)

input()
