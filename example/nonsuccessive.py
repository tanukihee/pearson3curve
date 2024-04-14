import os

import pearson3curve as p3
import pearson3curve.pgfplot as p3plot

# 本例取自《工程水文学》（2000年第3版，詹道江 叶守泽 主编）P242表9-4
# 注：表中第Ⅱ行流量2100应改为2200，第21行流量340应改为346
data = p3.Data(
    [
        1400,
        1210,
        960,
        920,
        890,
        880,
        790,
        784,
        670,
        650,
        638,
        590,
        520,
        510,
        480,
        470,
        462,
        440,
        386,
        368,
        346,
        322,
        300,
        288,
        262,
        240,
        220,
        200,
        186,
        160,
    ]
)

data.set_history_data([2520, 2200], 102)

mex, mcv, mcs = p3.get_moments(data)
fex, fcv, fcs = p3.get_fitted_moments(data, moments=(mex, mcv, mcs))

p3plot.set_figsize(7, 5)


p3plot.set_tex_preamble(
    r"""
    \usepackage{xeCJK}
    \setCJKmainfont{Source Han Sans SC}
    \usepackage{unicode-math}
    \setmathfont{Fira Math}
    \setsansfont{Fira Sans}
    \usepackage{siunitx}
    \sisetup{detect-all}
    """
)

p3plot.set_title("P-III曲线示例")
p3plot.set_xlabel(r"频率$P$ (\%)")
p3plot.set_ylabel(r"流量$Q$ (\si{\cubic\meter\per\second})")

p3plot.scatter(data, extreme_label="特大洪水数据", ordinary_label="一般洪水数据")

p3plot.plot(p3.Curve(mex, mcv, mcs), label="矩法估计曲线", linestyle="--")
p3plot.plot(p3.Curve(fex, fcv, fcs), label="适线后曲线")

p3plot.legend()
p3plot.save("example/nonsuccessive.pdf", transparent=False)
os.system("pdf2svg example/nonsuccessive.pdf example/nonsuccessive.svg")
os.remove("example/nonsuccessive.pdf")
