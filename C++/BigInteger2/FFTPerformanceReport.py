#vim:fileencoding=utf-8

import re
import matplotlib.pyplot as plt

double_precision_benchmark = [
"Scan v0\n\
        2^2: 0.079962 us 2^3: 0.150466 us 2^4: 0.311328 us 2^5: 0.682485 us 2^6: 1.510509 us 2^7: 3.264630 us 2^8: 7.021524 us 2^9: 15.282907 us 2^10: 32.847624 us 2^11: 72.555466 us 2^12: 153.917699 us 2^13: 324.635527 us 2^14: 729.209387 us 2^15: 1542.160453 us 2^16: 3264.870484 us 2^17: 7081.932187 us 2^18: 20505.781062 us 2^19: 49105.946875 us 2^20: 103019.066000 us 2^21: 214132.931500 us 2^22: 443331.132000 us 2^23: 954920.208000 us 2^24: 1957818.870000 us",
"Scan v1\n\
        2^2: 0.141517 us 2^3: 0.155555 us 2^4: 0.221316 us 2^5: 0.378981 us 2^6: 0.690240 us 2^7: 1.380858 us 2^8: 2.801186 us 2^9: 5.772764 us 2^10: 11.988426 us 2^11: 25.936346 us 2^12: 60.201833 us 2^13: 134.466947 us 2^14: 315.573324 us 2^15: 740.476961 us 2^16: 1700.749328 us 2^17: 3954.565656 us 2^18: 9000.179125 us 2^19: 29789.942625 us 2^20: 94984.762250 us 2^21: 231787.832000 us 2^22: 531270.086000 us 2^23: 1164032.236000 us 2^24: 2576454.446000 us",
"Scan v2\n\
        2^2: 0.006325 us 2^3: 0.014680 us 2^4: 0.034214 us 2^5: 0.075677 us 2^6: 0.163365 us 2^7: 0.515918 us 2^8: 1.573504 us 2^9: 2.913456 us 2^10: 6.965794 us 2^11: 16.919167 us 2^12: 38.455956 us 2^13: 88.046469 us 2^14: 209.365953 us 2^15: 440.720859 us 2^16: 965.442359 us 2^17: 2069.598781 us 2^18: 4976.491875 us 2^19: 14596.411125 us 2^20: 33968.353000 us 2^21: 71746.794500 us 2^22: 159853.750000 us 2^23: 379361.668000 us 2^24: 802336.167000 us",
"Scan v3\n\
        2^2: 0.006249 us 2^3: 0.012005 us 2^4: 0.027499 us 2^5: 0.061806 us 2^6: 0.141250 us 2^7: 0.330654 us 2^8: 0.719489 us 2^9: 2.080796 us 2^10: 4.617107 us 2^11: 11.999167 us 2^12: 27.076258 us 2^13: 60.027029 us 2^14: 144.517067 us 2^15: 310.926564 us 2^16: 673.072805 us 2^17: 1500.501492 us 2^18: 3652.441172 us 2^19: 11368.884281 us 2^20: 31918.040562 us 2^21: 65311.403625 us 2^22: 123355.433250 us 2^23: 280407.102500 us 2^24: 606104.036000 us",
"fftw3 estimate\n\
        2^2: 0.019903 us 2^3: 0.027295 us 2^4: 0.045500 us 2^5: 0.082414 us 2^6: 0.120721 us 2^7: 0.237984 us 2^8: 0.509205 us 2^9: 1.122954 us 2^10: 2.552185 us 2^11: 6.417468 us 2^12: 18.225350 us 2^13: 44.843113 us 2^14: 100.384066 us 2^15: 227.192547 us 2^16: 520.935828 us 2^17: 1185.360187 us 2^18: 3300.773187 us 2^19: 15199.068750 us 2^20: 34158.729500 us 2^21: 78615.560500 us 2^22: 199265.495000 us 2^23: 468799.826000 us 2^24: 1036200.585000 us",
"fftw3 measure\n\
        2^2: 0.009581 us 2^3: 0.014884 us 2^4: 0.030869 us 2^5: 0.057567 us 2^6: 0.101685 us 2^7: 0.211407 us 2^8: 0.441372 us 2^9: 1.006859 us 2^10: 2.435206 us 2^11: 5.973245 us 2^12: 15.925809 us 2^13: 36.915670 us 2^14: 93.872133 us 2^15: 193.272102 us 2^16: 419.216875 us 2^17: 951.608625 us 2^18: 3010.650813 us 2^19: 11666.031750 us 2^20: 21018.392250 us 2^21: 48927.700000 us 2^22: 99816.569000 us 2^23: 209901.861000 us 2^24: 461945.373000 us",
"acm tempate\n\
        2^2: 0.062168 us 2^3: 0.117608 us 2^4: 0.221078 us 2^5: 0.449748 us 2^6: 0.942373 us 2^7: 2.095933 us 2^8: 4.746445 us 2^9: 10.357794 us 2^10: 22.766678 us 2^11: 50.627132 us 2^12: 114.096557 us 2^13: 251.487518 us 2^14: 553.358938 us 2^15: 1228.570609 us 2^16: 2556.063266 us 2^17: 5306.420406 us 2^18: 11467.462562 us 2^19: 28298.686375 us 2^20: 65082.793750 us 2^21: 135470.812000 us 2^22: 281737.100000 us 2^23: 602935.668000 us 2^24: 1250711.256000 us",
"acm slow\n\
        2^2: 0.707088 us 2^3: 1.555619 us 2^4: 3.265494 us 2^5: 6.849430 us 2^6: 13.740353 us 2^7: 28.782172 us 2^8: 57.539458 us 2^9: 115.768977 us 2^10: 235.364391 us 2^11: 482.533722 us 2^12: 982.671263 us 2^13: 2087.221148 us 2^14: 4228.394109 us 2^15: 8471.245852 us 2^16: 17563.286562 us 2^17: 35952.604594 us 2^18: 75374.341500 us 2^19: 155452.267000 us 2^20: 322945.178750 us 2^21: 671607.813000 us 2^22: 1428045.276000 us 2^23: 2928475.751000 us 2^24: 5983035.637000 us",
"cpp cookbook\n\
        2^2: 0.109812 us 2^3: 0.189425 us 2^4: 0.317168 us 2^5: 0.556417 us 2^6: 1.107081 us 2^7: 2.236040 us 2^8: 4.751227 us 2^9: 10.334803 us 2^10: 23.186108 us 2^11: 52.842949 us 2^12: 157.894957 us 2^13: 389.784287 us 2^14: 965.509461 us 2^15: 2446.219719 us 2^16: 6446.361859 us 2^17: 15417.762312 us 2^18: 35176.060063 us 2^19: 80675.648500 us 2^20: 208856.786750 us 2^21: 483802.265500 us 2^22: 1029341.612000 us 2^23: 2272183.478000 us 2^24: 5715041.494000 us",
"free small fft\n\
        2^2: 0.141422 us 2^3: 0.261944 us 2^4: 0.520917 us 2^5: 1.016602 us 2^6: 2.057630 us 2^7: 4.335238 us 2^8: 9.079623 us 2^9: 18.971435 us 2^10: 39.685183 us 2^11: 83.042304 us 2^12: 179.641425 us 2^13: 382.547236 us 2^14: 810.309562 us 2^15: 1820.245422 us 2^16: 4264.939578 us 2^17: 9548.321031 us 2^18: 22092.093625 us 2^19: 57197.581875 us 2^20: 154132.439750 us 2^21: 367135.242000 us 2^22: 832086.106000 us 2^23: 1825193.081000 us 2^24: 4042984.221000 us",
"Eigen C++\n\
        2^2: 0.029143 us 2^3: 0.073629 us 2^4: 0.165334 us 2^5: 0.392684 us 2^6: 0.860470 us 2^7: 2.099621 us 2^8: 4.422548 us 2^9: 9.733137 us 2^10: 20.943952 us 2^11: 46.830123 us 2^12: 97.514787 us 2^13: 217.099166 us 2^14: 467.944555 us 2^15: 1018.298258 us 2^16: 2294.098047 us 2^17: 5509.359188 us 2^18: 17931.745188 us 2^19: 39482.750375 us 2^20: 101062.642000 us 2^21: 241127.799500 us 2^22: 565558.923000 us 2^23: 1274752.164000 us 2^24: 2869562.899000 us",
        ]

single_precision_benchmark = [
"Scan v1\n\
        2^2: 0.159404 us 2^3: 0.177322 us 2^4: 0.262283 us 2^5: 0.473721 us 2^6: 0.939148 us 2^7: 1.937010 us 2^8: 4.091349 us 2^9: 8.768141 us 2^10: 18.853335 us 2^11: 40.265807 us 2^12: 87.621302 us 2^13: 199.418391 us 2^14: 440.320927 us 2^15: 954.351947 us 2^16: 2168.117090 us 2^17: 5424.435656 us 2^18: 12194.887453 us 2^19: 26896.629063 us 2^20: 68957.125625 us 2^21: 198153.824125 us 2^22: 492545.715250 us 2^23: 1166968.717500 us 2^24: 2706565.189000 us",
"Scan v3\n\
        2^2: 0.006235 us 2^3: 0.012129 us 2^4: 0.024907 us 2^5: 0.054932 us 2^6: 0.121624 us 2^7: 0.255152 us 2^8: 0.563330 us 2^9: 1.691126 us 2^10: 3.548210 us 2^11: 7.395634 us 2^12: 19.350694 us 2^13: 48.313318 us 2^14: 102.257480 us 2^15: 254.393285 us 2^16: 524.988711 us 2^17: 1110.529453 us 2^18: 2431.456031 us 2^19: 5512.127812 us 2^20: 16971.501125 us 2^21: 47978.078250 us 2^22: 95459.083500 us 2^23: 210215.713500 us 2^24: 543143.784000 us",
"acm template\n\
        2^2: 0.064891 us 2^3: 0.124022 us 2^4: 0.223864 us 2^5: 0.460233 us 2^6: 0.992844 us 2^7: 2.166612 us 2^8: 4.803569 us 2^9: 10.621390 us 2^10: 23.154638 us 2^11: 51.092286 us 2^12: 112.842904 us 2^13: 249.646767 us 2^14: 548.235443 us 2^15: 1187.453141 us 2^16: 2638.447703 us 2^17: 5495.939789 us 2^18: 11450.050359 us 2^19: 24290.028813 us 2^20: 57381.912375 us 2^21: 125422.338625 us 2^22: 262010.057750 us 2^23: 541566.079500 us 2^24: 1134684.294000 us",
"Eigen C++\n\
        2^2: 0.026134 us 2^3: 0.073262 us 2^4: 0.134978 us 2^5: 0.368059 us 2^6: 0.701454 us 2^7: 1.758627 us 2^8: 3.250545 us 2^9: 8.126867 us 2^10: 15.194971 us 2^11: 36.922658 us 2^12: 71.248622 us 2^13: 168.917688 us 2^14: 333.149186 us 2^15: 845.832676 us 2^16: 1748.003227 us 2^17: 4394.662648 us 2^18: 10209.873156 us 2^19: 32636.726313 us 2^20: 71857.200687 us 2^21: 187991.215500 us 2^22: 446277.709500 us 2^23: 1047718.542500 us 2^24: 2453191.226000 us",
"fftwf3 estimate\n\
        2^2: 0.020325 us 2^3: 0.028691 us 2^4: 0.048577 us 2^5: 0.089945 us 2^6: 0.073045 us 2^7: 0.139401 us 2^8: 0.284831 us 2^9: 0.613621 us 2^10: 1.276350 us 2^11: 2.942038 us 2^12: 9.514741 us 2^13: 26.840536 us 2^14: 56.687779 us 2^15: 142.039482 us 2^16: 327.777902 us 2^17: 746.292031 us 2^18: 1768.576094 us 2^19: 9208.448000 us 2^20: 25945.896188 us 2^21: 62642.104250 us 2^22: 149345.458000 us 2^23: 332507.088500 us 2^24: 871520.150000 us",
"fftwf3 measure\n\
        2^2: 0.014036 us 2^3: 0.024250 us 2^4: 0.049287 us 2^5: 0.040288 us 2^6: 0.063215 us 2^7: 0.124809 us 2^8: 0.242458 us 2^9: 0.535405 us 2^10: 1.220656 us 2^11: 2.889325 us 2^12: 6.811809 us 2^13: 21.647146 us 2^14: 49.816230 us 2^15: 135.047867 us 2^16: 284.333230 us 2^17: 624.290984 us 2^18: 1390.347188 us 2^19: 7953.128094 us 2^20: 17005.082500 us 2^21: 37795.015500 us 2^22: 77346.360250 us 2^23: 168548.984500 us 2^24: 383664.308000 us",
"sleepwalking\n\
 2^2: 0.026250 us 2^3: 0.090967 us 2^4: 0.108127 us 2^5: 0.150908 us 2^6: 0.231587 us 2^7: 0.423333 us 2^8: 0.816786 us 2^9: 1.756054 us 2^10: 3.757429 us 2^11: 8.361273 us 2^12: 19.613903 us 2^13: 43.967512 us 2^14: 107.302417 us 2^15: 256.811400 us 2^16: 592.159195 us 2^17: 1396.124625 us 2^18: 4205.577859 us 2^19: 10325.939344 us 2^20: 22002.867063 us 2^21: 71785.297125 us 2^22: 2453191000000.0 us 2^23: 2453191000000.0 us 2^24: 2453191000000.0 us",
        ]

ys = []
names = []
for o in single_precision_benchmark:
    name, numStr = o.split('\n')
    y=[float(s) for s in re.findall('\d+\.\d+', numStr)]
    names.append(name.strip())
    ys.append(y)

x = range(2,len(ys[0])+2)

for y in ys:
    y2 = [(1<<i)*i*5/v for i,v in zip(x, y)]
    plt.plot(x, y2)

plt.legend(names)
plt.show()
