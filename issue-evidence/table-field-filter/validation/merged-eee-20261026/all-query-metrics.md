# Query metrics / 查询指标

Open=filehandle;plan includes metadata;full includes oracle and teardown. close only calls destroy_query_data_set;actual header releases can occur earlier during exhausted-device iteration. Correlated per-query P50/P95,whole-process memory. Old8 lack phase/individual quantiles/memory. / 打开仅句柄，计划含元数据，完整延迟含核对及销毁；close只计destroy_query_data_set，实际头部释放可在设备遍历耗尽时发生。P50/P95为相关查询描述值，内存为整进程；旧8项仍缺分项、单次分位数和内存。

| Matrix | Case | Stage | Version | Open ms P50/P95 | Plan ms P50/P95 | First ms P50/P95 | Close ms P50/P95 | Full ms P50/P95 | Rows/s | Peak MiB |
|---|---|---|---|---|---|---|---|---|---|---|
| standard96 | dense-w1-p0-b0 | initial | base | 0.0527/0.5893 | 0.0155/0.0529 | N/A | N/A | 7.8750/8.5547 | 0.00 | 4.955 |
| standard96 | dense-w1-p0-b0 | initial | prior | 0.0441/0.5683 | 0.0122/0.0561 | N/A | N/A | 0.5016/1.2048 | 0.00 | 4.906 |
| standard96 | dense-w1-p0-b0 | initial | public | 0.0465/0.5679 | 0.0120/0.0572 | N/A | N/A | 0.5156/1.2548 | 0.00 | 4.914 |
| standard96 | dense-w1-p0-b0 | initial | fixed | 0.0448/0.5876 | 0.0119/0.0541 | N/A | N/A | 0.5199/1.2145 | 0.00 | 4.916 |
| standard96 | dense-w1-p0-b1024 | initial | base | 0.0550/0.5537 | 0.0154/0.0499 | N/A | N/A | 7.8129/8.3728 | 0.00 | 4.953 |
| standard96 | dense-w1-p0-b1024 | initial | prior | 0.0442/0.5628 | 0.0121/0.0554 | N/A | N/A | 0.5149/1.1689 | 0.00 | 4.906 |
| standard96 | dense-w1-p0-b1024 | initial | public | 0.0432/0.5570 | 0.0119/0.0544 | N/A | N/A | 0.5072/1.1770 | 0.00 | 4.908 |
| standard96 | dense-w1-p0-b1024 | initial | fixed | 0.0430/0.5634 | 0.0126/0.0538 | N/A | N/A | 0.4997/1.1896 | 0.00 | 4.902 |
| standard96 | dense-w1-p1-b0 | initial | base | 0.0611/0.5434 | 0.0151/0.0483 | 3.8990/4.4266 | N/A | 7.7851/8.3707 | 50605.69 | 4.961 |
| standard96 | dense-w1-p1-b0 | initial | prior | 0.0482/0.5574 | 0.0123/0.0540 | 1.1117/1.7713 | N/A | 2.2086/2.9101 | 166809.17 | 5.037 |
| standard96 | dense-w1-p1-b0 | initial | public | 0.0472/0.5424 | 0.0127/0.0522 | 1.0524/1.6802 | N/A | 2.0921/2.7480 | 175698.12 | 5.020 |
| standard96 | dense-w1-p1-b0 | initial | fixed | 0.0471/0.5594 | 0.0125/0.0527 | 1.0381/1.7176 | N/A | 2.0603/2.7700 | 177805.64 | 5.059 |
| standard96 | dense-w1-p1-b1024 | initial | base | 0.0517/0.5522 | 0.0143/0.0485 | 3.8796/4.4458 | N/A | 7.7216/8.3830 | 50981.39 | 4.961 |
| standard96 | dense-w1-p1-b1024 | initial | prior | 0.0471/0.5496 | 0.0127/0.0549 | 1.1201/1.7809 | N/A | 2.1854/2.9038 | 168802.50 | 5.027 |
| standard96 | dense-w1-p1-b1024 | initial | public | 0.0474/0.5525 | 0.0119/0.0528 | 1.0565/1.7004 | N/A | 2.0922/2.7600 | 176216.63 | 5.078 |
| standard96 | dense-w1-p1-b1024 | initial | fixed | 0.0471/0.5836 | 0.0125/0.0531 | 1.0433/1.7172 | N/A | 2.0577/2.7720 | 178430.90 | 5.074 |
| standard96 | dense-w1-p10-b0 | initial | base | 0.0512/0.5579 | 0.0151/0.0460 | 2.0676/2.6456 | N/A | 8.3662/9.0318 | 472029.46 | 4.998 |
| standard96 | dense-w1-p10-b0 | initial | prior | 0.0471/0.5429 | 0.0132/0.0515 | 1.1418/1.7654 | N/A | 2.4519/3.1367 | 1518737.55 | 5.076 |
| standard96 | dense-w1-p10-b0 | initial | public | 0.0498/0.5582 | 0.0139/0.0499 | 1.0804/1.7176 | N/A | 2.3433/3.0186 | 1588815.36 | 5.062 |
| standard96 | dense-w1-p10-b0 | initial | fixed | 0.0512/0.5265 | 0.0140/0.0513 | 1.0722/1.7002 | N/A | 2.3178/2.9810 | 1606576.57 | 5.076 |
| standard96 | dense-w1-p10-b1024 | initial | base | 0.0609/0.5441 | 0.0142/0.0501 | 2.0999/2.6787 | N/A | 7.9520/8.6997 | 501528.66 | 4.996 |
| standard96 | dense-w1-p10-b1024 | initial | prior | 0.0483/0.5734 | 0.0115/0.0543 | 1.1404/1.8107 | N/A | 2.2785/3.0063 | 1618659.03 | 5.086 |
| standard96 | dense-w1-p10-b1024 | initial | public | 0.0467/0.5862 | 0.0130/0.0510 | 1.0818/1.7520 | N/A | 2.1738/2.9069 | 1688298.19 | 5.062 |
| standard96 | dense-w1-p10-b1024 | initial | fixed | 0.0473/0.5665 | 0.0115/0.0528 | 1.0684/1.7201 | N/A | 2.1503/2.8382 | 1720160.66 | 5.070 |
| standard96 | dense-w1-p50-b0 | initial | base | 0.0599/0.5567 | 0.0148/0.0486 | 0.5411/1.1435 | N/A | 11.1316/11.6285 | 1801217.63 | 5.480 |
| standard96 | dense-w1-p50-b0 | initial | prior | 0.0503/0.5482 | 0.0123/0.0547 | 0.6956/1.3452 | N/A | 3.4802/4.1743 | 5456951.57 | 5.301 |
| standard96 | dense-w1-p50-b0 | initial | public | 0.0493/0.5638 | 0.0117/0.0509 | 0.6593/1.2846 | N/A | 3.3279/4.0179 | 5695571.73 | 5.355 |
| standard96 | dense-w1-p50-b0 | initial | fixed | 0.0482/0.5710 | 0.0136/0.0519 | 0.6680/1.2945 | N/A | 3.3188/4.1892 | 5699685.22 | 5.293 |
| standard96 | dense-w1-p50-b1024 | initial | base | 0.0603/0.5371 | 0.0158/0.0454 | 0.5447/1.0932 | N/A | 8.2763/8.8969 | 2394777.13 | 5.195 |
| standard96 | dense-w1-p50-b1024 | initial | prior | 0.0495/0.5486 | 0.0145/0.0521 | 0.6997/1.3003 | N/A | 2.5730/3.2664 | 7272740.46 | 5.352 |
| standard96 | dense-w1-p50-b1024 | initial | public | 0.0488/0.5587 | 0.0158/0.0531 | 0.6572/1.2833 | N/A | 2.4165/3.1537 | 7676378.59 | 5.359 |
| standard96 | dense-w1-p50-b1024 | initial | fixed | 0.0487/0.5708 | 0.0160/0.0495 | 0.6629/1.2847 | N/A | 2.3863/3.1020 | 7822432.50 | 5.367 |
| standard96 | dense-w1-p100-b0 | initial | base | 0.0631/0.5769 | 0.0172/0.0521 | 0.3671/0.9879 | N/A | 14.2659/14.7843 | 2813322.51 | 5.641 |
| standard96 | dense-w1-p100-b0 | initial | prior | 0.0516/0.5746 | 0.0137/0.0529 | 0.5901/1.2335 | N/A | 4.0316/4.8109 | 9439491.85 | 5.775 |
| standard96 | dense-w1-p100-b0 | initial | public | 0.0524/0.5621 | 0.0150/0.0521 | 0.5927/1.2123 | N/A | 4.0340/4.7607 | 9480696.93 | 5.883 |
| standard96 | dense-w1-p100-b0 | initial | fixed | 0.0507/0.5588 | 0.0152/0.0512 | 0.5882/1.2228 | N/A | 4.0205/4.7484 | 9543278.93 | 5.781 |
| standard96 | dense-w1-p100-b1024 | initial | base | 0.0610/0.5687 | 0.0144/0.0497 | 0.3685/0.9568 | N/A | 8.9074/9.6368 | 4473798.30 | 5.410 |
| standard96 | dense-w1-p100-b1024 | initial | prior | 0.0498/0.5555 | 0.0113/0.0532 | 0.5745/1.2132 | N/A | 2.2316/2.9596 | 16467579.79 | 5.777 |
| standard96 | dense-w1-p100-b1024 | initial | public | 0.0501/0.5778 | 0.0137/0.0520 | 0.5850/1.2084 | N/A | 2.2428/2.9863 | 16528819.16 | 5.879 |
| standard96 | dense-w1-p100-b1024 | initial | fixed | 0.0492/0.5717 | 0.0136/0.0533 | 0.5809/1.2326 | N/A | 2.2085/2.9787 | 16679558.99 | 5.770 |
| standard96 | dense-w4-p0-b0 | initial | base | 0.0646/0.5537 | 0.0194/0.0495 | N/A | N/A | 17.3416/17.9291 | 0.00 | 5.523 |
| standard96 | dense-w4-p0-b0 | initial | prior | 0.0467/0.5667 | 0.0154/0.0563 | N/A | N/A | 1.0573/1.7772 | 0.00 | 4.938 |
| standard96 | dense-w4-p0-b0 | initial | public | 0.0463/0.5720 | 0.0162/0.0557 | N/A | N/A | 1.0721/1.7904 | 0.00 | 4.938 |
| standard96 | dense-w4-p0-b0 | initial | fixed | 0.0464/0.5661 | 0.0155/0.0542 | N/A | N/A | 1.0479/1.7686 | 0.00 | 4.941 |
| standard96 | dense-w4-p0-b1024 | initial | base | 0.0638/0.5577 | 0.0190/0.0499 | N/A | N/A | 17.1932/17.8357 | 0.00 | 5.520 |
| standard96 | dense-w4-p0-b1024 | initial | prior | 0.0461/0.5681 | 0.0156/0.0537 | N/A | N/A | 1.0383/1.7208 | 0.00 | 4.941 |
| standard96 | dense-w4-p0-b1024 | initial | public | 0.0459/0.5500 | 0.0158/0.0537 | N/A | N/A | 1.0409/1.7478 | 0.00 | 4.934 |
| standard96 | dense-w4-p0-b1024 | initial | fixed | 0.0454/0.5420 | 0.0159/0.0524 | N/A | N/A | 1.0345/1.7083 | 0.00 | 4.934 |
| standard96 | dense-w4-p1-b0 | initial | base | 0.0683/0.5775 | 0.0184/0.0527 | 8.4345/9.3520 | N/A | 17.3903/18.0513 | 23179.87 | 5.521 |
| standard96 | dense-w4-p1-b0 | initial | prior | 0.0521/0.5864 | 0.0135/0.0579 | 1.9737/2.7388 | N/A | 3.9566/4.7911 | 95491.63 | 5.188 |
| standard96 | dense-w4-p1-b0 | initial | public | 0.0540/0.5825 | 0.0150/0.0570 | 1.9165/2.6680 | N/A | 3.8553/4.6860 | 97852.17 | 5.174 |
| standard96 | dense-w4-p1-b0 | initial | fixed | 0.0546/0.5858 | 0.0160/0.0558 | 1.9008/2.7185 | N/A | 3.8176/4.7606 | 98672.45 | 5.186 |
| standard96 | dense-w4-p1-b1024 | initial | base | 0.0673/0.5661 | 0.0199/0.0513 | 8.5582/9.3191 | N/A | 17.2273/17.9335 | 23249.96 | 5.539 |
| standard96 | dense-w4-p1-b1024 | initial | prior | 0.0530/0.5717 | 0.0168/0.0559 | 1.9804/2.6989 | N/A | 3.8972/4.7232 | 97758.50 | 5.180 |
| standard96 | dense-w4-p1-b1024 | initial | public | 0.0546/0.5765 | 0.0177/0.0553 | 1.9122/2.6793 | N/A | 3.7740/4.6870 | 100807.30 | 5.160 |
| standard96 | dense-w4-p1-b1024 | initial | fixed | 0.0521/0.5652 | 0.0175/0.0554 | 1.9084/2.6092 | N/A | 3.7485/4.5567 | 101422.45 | 5.223 |
| standard96 | dense-w4-p10-b0 | initial | base | 0.0666/0.5665 | 0.0197/0.0517 | 4.5153/5.2532 | N/A | 18.6498/19.2563 | 216101.03 | 5.551 |
| standard96 | dense-w4-p10-b0 | initial | prior | 0.0527/0.5850 | 0.0153/0.0544 | 2.0189/2.7589 | N/A | 4.7833/5.6112 | 797880.35 | 5.246 |
| standard96 | dense-w4-p10-b0 | initial | public | 0.0532/0.5846 | 0.0168/0.0546 | 1.9904/2.6776 | N/A | 4.7144/5.5151 | 814713.94 | 5.238 |
| standard96 | dense-w4-p10-b0 | initial | fixed | 0.0539/0.5730 | 0.0160/0.0549 | 1.9350/2.6639 | N/A | 4.5985/5.4696 | 828426.42 | 5.273 |
| standard96 | dense-w4-p10-b1024 | initial | base | 0.0691/0.5673 | 0.0202/0.0498 | 4.5037/5.2325 | N/A | 17.5111/18.2944 | 228968.54 | 5.570 |
| standard96 | dense-w4-p10-b1024 | initial | prior | 0.0544/0.5668 | 0.0176/0.0555 | 2.0173/2.7659 | N/A | 4.0953/4.9866 | 928602.45 | 5.252 |
| standard96 | dense-w4-p10-b1024 | initial | public | 0.0559/0.5693 | 0.0174/0.0562 | 1.9498/2.6671 | N/A | 3.9735/4.7859 | 961442.79 | 5.238 |
| standard96 | dense-w4-p10-b1024 | initial | fixed | 0.0594/0.5748 | 0.0190/0.0543 | 1.9311/2.6586 | N/A | 3.9223/4.7712 | 965627.68 | 5.244 |
| standard96 | dense-w4-p50-b0 | initial | base | 0.0662/0.5741 | 0.0188/0.0474 | 1.1210/1.8025 | N/A | 23.3550/23.9952 | 861241.77 | 5.734 |
| standard96 | dense-w4-p50-b0 | initial | prior | 0.0637/0.5615 | 0.0180/0.0518 | 1.2330/1.8752 | N/A | 8.0820/8.9582 | 2408537.75 | 5.594 |
| standard96 | dense-w4-p50-b0 | initial | public | 0.0626/0.5767 | 0.0169/0.0530 | 1.2040/1.8521 | N/A | 8.0684/9.0446 | 2424918.57 | 5.660 |
| standard96 | dense-w4-p50-b0 | initial | fixed | 0.0594/0.5539 | 0.0177/0.0504 | 1.1971/1.8140 | N/A | 7.9641/8.7786 | 2445700.91 | 5.617 |
| standard96 | dense-w4-p50-b1024 | initial | base | 0.0649/0.5871 | 0.0182/0.0512 | 1.1266/1.8419 | N/A | 18.3870/19.1955 | 1093454.03 | 5.691 |
| standard96 | dense-w4-p50-b1024 | initial | prior | 0.0530/0.5869 | 0.0140/0.0554 | 1.2139/1.9197 | N/A | 4.7414/5.5863 | 4026429.64 | 5.559 |
| standard96 | dense-w4-p50-b1024 | initial | public | 0.0546/0.5945 | 0.0167/0.0537 | 1.2186/1.8619 | N/A | 4.6632/5.4877 | 4106652.30 | 5.605 |
| standard96 | dense-w4-p50-b1024 | initial | fixed | 0.0531/0.5729 | 0.0163/0.0540 | 1.1895/1.8351 | N/A | 4.5917/5.4652 | 4172375.32 | 5.559 |
| standard96 | dense-w4-p100-b0 | initial | base | 0.0772/0.5676 | 0.0185/0.0504 | 0.7286/1.3362 | N/A | 29.5626/30.1977 | 1356001.53 | 5.836 |
| standard96 | dense-w4-p100-b0 | initial | prior | 0.0691/0.5777 | 0.0170/0.0551 | 1.1024/1.7543 | N/A | 11.6726/12.3870 | 3461479.83 | 6.371 |
| standard96 | dense-w4-p100-b0 | initial | public | 0.0659/0.5878 | 0.0170/0.0552 | 1.0956/1.8087 | N/A | 11.7692/12.3755 | 3391933.03 | 6.395 |
| standard96 | dense-w4-p100-b0 | initial | fixed | 0.0666/0.5742 | 0.0170/0.0562 | 1.0684/1.7619 | N/A | 11.6547/12.1304 | 3447518.16 | 6.387 |
| standard96 | dense-w4-p100-b1024 | initial | base | 0.0699/0.5876 | 0.0196/0.0516 | 0.7251/1.4156 | N/A | 19.4076/20.2667 | 2062806.05 | 5.840 |
| standard96 | dense-w4-p100-b1024 | initial | prior | 0.0541/0.5730 | 0.0158/0.0547 | 1.0890/1.7609 | N/A | 4.4732/5.3161 | 8670746.41 | 6.016 |
| standard96 | dense-w4-p100-b1024 | initial | public | 0.0536/0.5940 | 0.0160/0.0541 | 1.0938/1.7839 | N/A | 4.4600/5.3500 | 8552120.18 | 6.031 |
| standard96 | dense-w4-p100-b1024 | initial | fixed | 0.0588/0.5585 | 0.0174/0.0537 | 1.0540/1.7317 | N/A | 4.3859/5.2088 | 8743585.13 | 6.023 |
| standard96 | dense-w8-p0-b0 | initial | base | 0.0856/0.5721 | 0.0245/0.0591 | N/A | N/A | 30.5309/32.7264 | 0.00 | 5.977 |
| standard96 | dense-w8-p0-b0 | initial | prior | 0.0503/0.5986 | 0.0202/0.0626 | N/A | N/A | 1.7311/2.6021 | 0.00 | 4.980 |
| standard96 | dense-w8-p0-b0 | initial | public | 0.0490/0.5835 | 0.0211/0.0640 | N/A | N/A | 1.7297/2.5323 | 0.00 | 4.969 |
| standard96 | dense-w8-p0-b0 | initial | fixed | 0.0508/0.5828 | 0.0213/0.0632 | N/A | N/A | 1.7300/2.5689 | 0.00 | 4.977 |
| standard96 | dense-w8-p0-b1024 | initial | base | 0.0707/0.5529 | 0.0246/0.0585 | N/A | N/A | 30.0030/31.3612 | 0.00 | 5.951 |
| standard96 | dense-w8-p0-b1024 | initial | prior | 0.0496/0.5621 | 0.0194/0.0616 | N/A | N/A | 1.6780/2.4620 | 0.00 | 4.973 |
| standard96 | dense-w8-p0-b1024 | initial | public | 0.0493/0.5690 | 0.0207/0.0619 | N/A | N/A | 1.6991/2.4830 | 0.00 | 4.969 |
| standard96 | dense-w8-p0-b1024 | initial | fixed | 0.0475/0.5667 | 0.0210/0.0605 | N/A | N/A | 1.6761/2.4704 | 0.00 | 4.973 |
| standard96 | dense-w8-p1-b0 | initial | base | 0.0745/0.6442 | 0.0261/0.0598 | 15.4420/16.1190 | N/A | 30.6964/32.3920 | 13109.69 | 6.008 |
| standard96 | dense-w8-p1-b0 | initial | prior | 0.0612/0.6040 | 0.0219/0.0647 | 3.1883/4.1191 | N/A | 6.4746/7.5632 | 59432.99 | 5.297 |
| standard96 | dense-w8-p1-b0 | initial | public | 0.0631/0.5986 | 0.0263/0.0648 | 3.1132/4.3203 | N/A | 6.2649/7.8134 | 60993.28 | 5.262 |
| standard96 | dense-w8-p1-b0 | initial | fixed | 0.0584/0.5850 | 0.0258/0.0620 | 3.1029/4.0092 | N/A | 6.2357/7.4284 | 61377.00 | 5.299 |
| standard96 | dense-w8-p1-b1024 | initial | base | 0.0740/0.5728 | 0.0241/0.0610 | 15.4764/16.2463 | N/A | 30.6371/32.3917 | 13133.66 | 5.990 |
| standard96 | dense-w8-p1-b1024 | initial | prior | 0.0558/0.5907 | 0.0209/0.0646 | 3.1625/4.0409 | N/A | 6.2299/7.2942 | 61489.11 | 5.297 |
| standard96 | dense-w8-p1-b1024 | initial | public | 0.0594/0.5839 | 0.0230/0.0628 | 3.0817/4.0149 | N/A | 6.0778/7.2500 | 62603.35 | 5.283 |
| standard96 | dense-w8-p1-b1024 | initial | fixed | 0.0595/0.5735 | 0.0231/0.0607 | 3.0599/3.9415 | N/A | 6.0307/7.1826 | 63029.89 | 5.293 |
| standard96 | dense-w8-p10-b0 | initial | base | 0.0744/0.5919 | 0.0221/0.0557 | 8.0572/8.9254 | N/A | 33.0015/34.9066 | 122401.11 | 6.078 |
| standard96 | dense-w8-p10-b0 | initial | prior | 0.0628/0.5732 | 0.0199/0.0576 | 3.2017/4.0678 | N/A | 7.8868/9.0022 | 488586.86 | 5.416 |
| standard96 | dense-w8-p10-b0 | initial | public | 0.0592/0.6011 | 0.0238/0.0604 | 3.1407/4.0664 | N/A | 7.8067/8.9727 | 495315.15 | 5.383 |
| standard96 | dense-w8-p10-b0 | initial | fixed | 0.0640/0.5837 | 0.0236/0.0581 | 3.1284/4.0197 | N/A | 7.7860/8.9078 | 497122.94 | 5.391 |
| standard96 | dense-w8-p10-b1024 | initial | base | 0.0731/0.5504 | 0.0262/0.0550 | 8.2854/8.9130 | N/A | 30.7420/33.0234 | 130366.71 | 6.059 |
| standard96 | dense-w8-p10-b1024 | initial | prior | 0.0644/0.5736 | 0.0218/0.0607 | 3.2217/4.0936 | N/A | 6.5401/7.6452 | 585505.86 | 5.404 |
| standard96 | dense-w8-p10-b1024 | initial | public | 0.0562/0.5872 | 0.0229/0.0614 | 3.1538/4.0757 | N/A | 6.4329/7.6949 | 596920.04 | 5.387 |
| standard96 | dense-w8-p10-b1024 | initial | fixed | 0.0577/0.6024 | 0.0221/0.0592 | 3.1393/4.0366 | N/A | 6.4015/7.5501 | 597474.25 | 5.395 |
| standard96 | dense-w8-p50-b0 | initial | base | 0.0785/0.5894 | 0.0226/0.0533 | 1.9483/2.7153 | N/A | 41.3936/43.5552 | 485723.63 | 6.240 |
| standard96 | dense-w8-p50-b0 | initial | prior | 0.0686/0.5725 | 0.0252/0.0573 | 1.9796/2.6921 | N/A | 15.0196/15.6986 | 1335586.26 | 6.234 |
| standard96 | dense-w8-p50-b0 | initial | public | 0.0667/0.5670 | 0.0269/0.0594 | 1.9333/2.6072 | N/A | 14.7204/15.5063 | 1351654.36 | 6.227 |
| standard96 | dense-w8-p50-b0 | initial | fixed | 0.0670/0.5697 | 0.0251/0.0573 | 1.9111/2.6006 | N/A | 14.6933/15.3871 | 1369653.55 | 6.225 |
| standard96 | dense-w8-p50-b1024 | initial | base | 0.0737/0.5801 | 0.0239/0.0575 | 1.9623/2.7131 | N/A | 32.3805/34.7336 | 617951.83 | 6.186 |
| standard96 | dense-w8-p50-b1024 | initial | prior | 0.0572/0.5897 | 0.0226/0.0600 | 1.9355/2.6747 | N/A | 7.6227/8.7178 | 2541893.79 | 5.840 |
| standard96 | dense-w8-p50-b1024 | initial | public | 0.0605/0.5914 | 0.0244/0.0595 | 1.8721/2.6286 | N/A | 7.4589/8.6224 | 2579514.02 | 5.879 |
| standard96 | dense-w8-p50-b1024 | initial | fixed | 0.0564/0.5793 | 0.0252/0.0586 | 1.8747/2.6341 | N/A | 7.4721/8.5761 | 2592195.80 | 5.855 |
| standard96 | dense-w8-p100-b0 | initial | base | 0.0850/0.5571 | 0.0238/0.0569 | 1.2267/1.8373 | N/A | 52.0437/54.1219 | 768879.21 | 6.344 |
| standard96 | dense-w8-p100-b0 | initial | prior | 0.0823/0.5666 | 0.0254/0.0623 | 1.8185/2.5079 | N/A | 21.9886/22.6342 | 1829144.27 | 6.873 |
| standard96 | dense-w8-p100-b0 | initial | public | 0.0771/0.5617 | 0.0284/0.0603 | 1.8057/2.4866 | N/A | 21.8076/22.5132 | 1842367.07 | 6.857 |
| standard96 | dense-w8-p100-b0 | initial | fixed | 0.0795/0.5990 | 0.0270/0.0605 | 1.7992/2.5394 | N/A | 21.5518/22.2828 | 1855212.23 | 6.881 |
| standard96 | dense-w8-p100-b1024 | initial | base | 0.0742/0.6191 | 0.0227/0.0572 | 1.2062/1.9181 | N/A | 34.2668/36.5129 | 1169202.63 | 6.336 |
| standard96 | dense-w8-p100-b1024 | initial | prior | 0.0628/0.6002 | 0.0220/0.0611 | 1.7332/2.4925 | N/A | 7.3291/8.4938 | 5277381.46 | 6.523 |
| standard96 | dense-w8-p100-b1024 | initial | public | 0.0592/0.5797 | 0.0239/0.0616 | 1.6985/2.4454 | N/A | 7.3136/8.4415 | 5284517.20 | 6.506 |
| standard96 | dense-w8-p100-b1024 | initial | fixed | 0.0639/0.5898 | 0.0248/0.0602 | 1.6994/2.5104 | N/A | 7.2682/8.4394 | 5281620.40 | 6.520 |
| standard96 | null-w1-p10-b0 | initial | base | 0.0606/0.5756 | 0.0148/0.0511 | 4.1653/4.6953 | N/A | 8.3098/8.9538 | 68241.74 | 4.961 |
| standard96 | null-w1-p10-b0 | initial | prior | 0.0481/0.5442 | 0.0116/0.0567 | 1.2372/1.9052 | N/A | 2.4384/3.1575 | 216261.19 | 5.035 |
| standard96 | null-w1-p10-b0 | initial | public | 0.0479/0.5745 | 0.0119/0.0561 | 1.1458/1.8168 | N/A | 2.2523/2.9647 | 233607.68 | 5.012 |
| standard96 | null-w1-p10-b0 | initial | fixed | 0.0553/0.5547 | 0.0122/0.0561 | 1.1492/1.8052 | N/A | 2.2457/2.9275 | 234774.24 | 5.029 |
| standard96 | null-w1-p10-b1024 | initial | base | 0.0572/0.5549 | 0.0144/0.0489 | 4.1558/4.7614 | N/A | 8.2545/8.8346 | 68997.55 | 4.963 |
| standard96 | null-w1-p10-b1024 | initial | prior | 0.0479/0.5894 | 0.0161/0.0583 | 1.2484/1.9743 | N/A | 2.4392/3.2398 | 214756.42 | 5.031 |
| standard96 | null-w1-p10-b1024 | initial | public | 0.0488/0.5813 | 0.0141/0.0543 | 1.1375/1.7817 | N/A | 2.2363/2.9308 | 234267.85 | 5.012 |
| standard96 | null-w1-p10-b1024 | initial | fixed | 0.0478/0.5521 | 0.0144/0.0551 | 1.1024/1.7763 | N/A | 2.1793/2.9526 | 241462.57 | 5.039 |
| standard96 | null-w1-p100-b0 | initial | base | 0.0602/0.5528 | 0.0146/0.0468 | 1.5660/2.1300 | N/A | 8.9055/9.3912 | 638237.56 | 5.012 |
| standard96 | null-w1-p100-b0 | initial | prior | 0.0467/0.5490 | 0.0123/0.0499 | 0.6999/1.3142 | N/A | 2.6638/3.3377 | 1997844.68 | 5.072 |
| standard96 | null-w1-p100-b0 | initial | public | 0.0469/0.5428 | 0.0132/0.0490 | 0.6533/1.2467 | N/A | 2.4365/3.0631 | 2189703.73 | 5.070 |
| standard96 | null-w1-p100-b0 | initial | fixed | 0.0467/0.5471 | 0.0132/0.0492 | 0.6443/1.2470 | N/A | 2.3850/3.0755 | 2221188.80 | 5.111 |
| standard96 | null-w1-p100-b1024 | initial | base | 0.0488/0.5339 | 0.0147/0.0473 | 1.5698/2.1207 | N/A | 8.2737/8.8617 | 681723.60 | 5.008 |
| standard96 | null-w1-p100-b1024 | initial | prior | 0.0468/0.5501 | 0.0138/0.0515 | 0.7037/1.3162 | N/A | 2.5483/3.2339 | 2077175.54 | 5.074 |
| standard96 | null-w1-p100-b1024 | initial | public | 0.0486/0.5502 | 0.0136/0.0494 | 0.6370/1.2466 | N/A | 2.3019/2.9551 | 2298628.79 | 5.074 |
| standard96 | null-w1-p100-b1024 | initial | fixed | 0.0482/0.5298 | 0.0160/0.0493 | 0.6352/1.2246 | N/A | 2.2904/2.9577 | 2299985.25 | 5.074 |
| standard96 | null-w8-p10-b0 | initial | base | 0.0786/0.5882 | 0.0241/0.0579 | 16.2425/17.2012 | N/A | 32.8984/35.2379 | 17498.09 | 5.949 |
| standard96 | null-w8-p10-b0 | initial | prior | 0.0576/0.5938 | 0.0232/0.0641 | 3.3006/4.2737 | N/A | 6.7096/7.9257 | 81505.12 | 5.297 |
| standard96 | null-w8-p10-b0 | initial | public | 0.0582/0.5807 | 0.0254/0.0615 | 3.1322/4.1010 | N/A | 6.3751/7.6543 | 85707.02 | 5.285 |
| standard96 | null-w8-p10-b0 | initial | fixed | 0.0628/0.5909 | 0.0257/0.0620 | 3.1124/4.1009 | N/A | 6.3405/7.6142 | 85708.85 | 5.273 |
| standard96 | null-w8-p10-b1024 | initial | base | 0.0755/0.6117 | 0.0244/0.0603 | 16.1842/17.3144 | N/A | 32.5824/34.6465 | 17532.25 | 5.965 |
| standard96 | null-w8-p10-b1024 | initial | prior | 0.0562/0.5954 | 0.0243/0.0640 | 3.3151/4.2908 | N/A | 6.5473/7.7452 | 83806.19 | 5.287 |
| standard96 | null-w8-p10-b1024 | initial | public | 0.0560/0.5739 | 0.0286/0.0652 | 3.1707/4.0927 | N/A | 6.2889/7.4537 | 86943.15 | 5.271 |
| standard96 | null-w8-p10-b1024 | initial | fixed | 0.0586/0.6044 | 0.0257/0.0632 | 3.1456/4.0965 | N/A | 6.2230/7.4429 | 87799.06 | 5.320 |
| standard96 | null-w8-p100-b0 | initial | base | 0.0671/0.5904 | 0.0224/0.0536 | 6.0320/6.8457 | N/A | 34.8974/37.3286 | 162301.75 | 6.047 |
| standard96 | null-w8-p100-b0 | initial | prior | 0.0631/0.5698 | 0.0250/0.0617 | 1.8008/2.5914 | N/A | 8.7349/9.8504 | 633823.52 | 5.416 |
| standard96 | null-w8-p100-b0 | initial | public | 0.0631/0.5709 | 0.0271/0.0630 | 1.7264/2.5181 | N/A | 8.3726/9.5958 | 658801.17 | 5.406 |
| standard96 | null-w8-p100-b0 | initial | fixed | 0.0629/0.5788 | 0.0268/0.0606 | 1.6956/2.4848 | N/A | 8.3001/9.4940 | 662298.63 | 5.430 |
| standard96 | null-w8-p100-b1024 | initial | base | 0.0786/0.5867 | 0.0234/0.0569 | 6.0882/7.0312 | N/A | 33.1157/35.7116 | 172615.30 | 6.049 |
| standard96 | null-w8-p100-b1024 | initial | prior | 0.0573/0.5965 | 0.0245/0.0623 | 1.8133/2.6182 | N/A | 6.9540/8.1312 | 791094.42 | 5.414 |
| standard96 | null-w8-p100-b1024 | initial | public | 0.0575/0.5977 | 0.0247/0.0629 | 1.7267/2.5357 | N/A | 6.6154/7.8586 | 825265.16 | 5.410 |
| standard96 | null-w8-p100-b1024 | initial | fixed | 0.0616/0.5742 | 0.0254/0.0606 | 1.7254/2.5178 | N/A | 6.6013/7.8018 | 824631.15 | 5.453 |
| standard96 | tag-parallel-s0-b0 | initial | base | 0.0654/0.5769 | 0.0237/0.0621 | 1.9278/2.6794 | N/A | 20.6248/21.3384 | 483716.88 | 5.992 |
| standard96 | tag-parallel-s0-b0 | initial | prior | 0.0682/0.5645 | 0.0251/0.0616 | 2.1967/3.2066 | N/A | 7.9729/9.0513 | 1221252.25 | 6.893 |
| standard96 | tag-parallel-s0-b0 | initial | public | 0.0643/0.5636 | 0.0244/0.0615 | 2.2510/3.2904 | N/A | 8.0037/9.2047 | 1215374.23 | 6.875 |
| standard96 | tag-parallel-s0-b0 | initial | fixed | 0.0621/0.5754 | 0.0242/0.0589 | 2.2356/3.2231 | N/A | 7.9663/9.0559 | 1222006.79 | 6.891 |
| standard96 | tag-parallel-s0-b1024 | initial | base | 0.0687/0.5861 | 0.0244/0.0636 | 1.9695/2.7179 | N/A | 16.4980/17.2626 | 607176.38 | 5.988 |
| standard96 | tag-parallel-s0-b1024 | initial | prior | 0.0630/0.5952 | 0.0250/0.0646 | 2.2283/3.2945 | N/A | 4.5894/5.8540 | 2070242.33 | 6.926 |
| standard96 | tag-parallel-s0-b1024 | initial | public | 0.0630/0.5813 | 0.0249/0.0629 | 2.2043/3.3705 | N/A | 4.5670/6.0392 | 2068317.04 | 6.875 |
| standard96 | tag-parallel-s0-b1024 | initial | fixed | 0.0619/0.6009 | 0.0249/0.0652 | 2.1926/3.3359 | N/A | 4.5495/5.7740 | 2086393.65 | 6.930 |
| standard96 | tag-parallel-s1-b0 | initial | base | 0.0690/0.5613 | 0.0249/0.0623 | 11.6990/12.7055 | N/A | 17.2055/18.0028 | 82822.83 | 5.922 |
| standard96 | tag-parallel-s1-b0 | initial | prior | 0.0587/0.5802 | 0.0249/0.0659 | 3.7045/4.8966 | N/A | 4.3704/5.5882 | 307139.43 | 6.633 |
| standard96 | tag-parallel-s1-b0 | initial | public | 0.0632/0.5873 | 0.0267/0.0657 | 3.7735/4.9532 | N/A | 4.4275/5.6451 | 304126.48 | 6.619 |
| standard96 | tag-parallel-s1-b0 | initial | fixed | 0.0604/0.5946 | 0.0254/0.0668 | 3.7353/5.0104 | N/A | 4.4003/5.7237 | 305963.09 | 6.629 |
| standard96 | tag-parallel-s1-b1024 | initial | base | 0.0651/0.5725 | 0.0238/0.0632 | 11.7781/12.7485 | N/A | 16.6896/17.5064 | 85997.74 | 5.898 |
| standard96 | tag-parallel-s1-b1024 | initial | prior | 0.0598/0.5549 | 0.0264/0.0634 | 3.6657/4.7625 | N/A | 3.8650/4.9839 | 344453.68 | 6.635 |
| standard96 | tag-parallel-s1-b1024 | initial | public | 0.0598/0.5578 | 0.0273/0.0645 | 3.7087/4.8226 | N/A | 3.9228/5.0733 | 342131.09 | 6.617 |
| standard96 | tag-parallel-s1-b1024 | initial | fixed | 0.0598/0.5681 | 0.0264/0.0631 | 3.6524/4.7282 | N/A | 3.8645/4.9601 | 345399.91 | 6.633 |
| standard96 | callback-w1-p1-b0 | initial | base | 0.0553/0.6067 | 0.0160/0.0505 | 3.9369/4.6086 | N/A | 7.8713/8.5966 | 49907.75 | 4.961 |
| standard96 | callback-w1-p1-b0 | initial | prior | 0.0610/0.5982 | 0.0150/0.0543 | 3.9738/4.6129 | N/A | 7.9504/8.6407 | 49590.62 | 4.969 |
| standard96 | callback-w1-p1-b0 | initial | public | 0.0621/0.5930 | 0.0157/0.0526 | 3.9859/4.5993 | N/A | 7.9699/8.6224 | 49529.14 | 4.977 |
| standard96 | callback-w1-p1-b0 | initial | fixed | 0.0608/0.6112 | 0.0146/0.0550 | 4.0190/4.6578 | N/A | 8.0084/8.6766 | 49192.23 | 4.977 |
| standard96 | callback-w1-p1-b1024 | initial | base | 0.0543/0.5622 | 0.0156/0.0485 | 3.9524/4.5454 | N/A | 7.8346/8.4735 | 50310.57 | 4.961 |
| standard96 | callback-w1-p1-b1024 | initial | prior | 0.0602/0.6037 | 0.0153/0.0523 | 3.9232/4.5658 | N/A | 7.7820/8.4600 | 50321.43 | 4.969 |
| standard96 | callback-w1-p1-b1024 | initial | public | 0.0568/0.5834 | 0.0150/0.0513 | 3.9526/4.5360 | N/A | 7.8259/8.4839 | 50335.15 | 4.973 |
| standard96 | callback-w1-p1-b1024 | initial | fixed | 0.0499/0.5695 | 0.0143/0.0520 | 3.9825/4.5781 | N/A | 7.9616/8.5233 | 50025.13 | 4.969 |
| standard96 | callback-w1-p100-b0 | initial | base | 0.0659/0.5650 | 0.0173/0.0491 | 0.3740/0.9645 | N/A | 14.3012/14.6336 | 2823669.80 | 5.641 |
| standard96 | callback-w1-p100-b0 | initial | prior | 0.0643/0.5882 | 0.0162/0.0510 | 0.3833/0.9889 | N/A | 14.2998/14.7434 | 2818941.13 | 5.637 |
| standard96 | callback-w1-p100-b0 | initial | public | 0.0619/0.5972 | 0.0146/0.0512 | 0.3695/1.0063 | N/A | 14.1940/14.6472 | 2835764.29 | 5.648 |
| standard96 | callback-w1-p100-b0 | initial | fixed | 0.0636/0.5603 | 0.0154/0.0496 | 0.3861/0.9533 | N/A | 14.3799/14.8703 | 2800942.46 | 5.637 |
| standard96 | callback-w1-p100-b0 | confirmations | base | 0.0614/0.5649 | 0.0166/0.0488 | 0.3638/0.9694 | N/A | 14.2000/14.5831 | 2826542.31 | 5.641 |
| standard96 | callback-w1-p100-b0 | confirmations | prior | 0.0627/0.5626 | 0.0157/0.0505 | 0.3775/0.9737 | N/A | 14.2281/15.0363 | 2823584.07 | 5.637 |
| standard96 | callback-w1-p100-b0 | confirmations | public | 0.0617/0.5658 | 0.0151/0.0506 | 0.3678/0.9786 | N/A | 14.1331/14.5513 | 2844637.49 | 5.648 |
| standard96 | callback-w1-p100-b0 | confirmations | fixed | 0.0616/0.5619 | 0.0155/0.0498 | 0.3795/0.9631 | N/A | 14.2957/14.8453 | 2805245.83 | 5.637 |
| standard96 | callback-w1-p100-b1024 | initial | base | 0.0606/0.5537 | 0.0153/0.0490 | 0.3661/0.9510 | N/A | 8.8911/9.4743 | 4498881.60 | 5.410 |
| standard96 | callback-w1-p100-b1024 | initial | prior | 0.0603/0.5651 | 0.0143/0.0508 | 0.3653/0.9601 | N/A | 8.8174/9.5228 | 4472088.92 | 5.277 |
| standard96 | callback-w1-p100-b1024 | initial | public | 0.0616/0.5829 | 0.0155/0.0520 | 0.3664/1.0005 | N/A | 8.8832/9.4958 | 4476158.88 | 5.285 |
| standard96 | callback-w1-p100-b1024 | initial | fixed | 0.0602/0.5602 | 0.0141/0.0490 | 0.3720/0.9584 | N/A | 9.0518/9.6847 | 4435417.96 | 5.523 |
| standard96 | callback-w1-p100-b1024 | confirmations | base | 0.0607/0.5612 | 0.0155/0.0496 | 0.3700/0.9613 | N/A | 8.8754/9.4759 | 4472113.58 | 5.410 |
| standard96 | callback-w1-p100-b1024 | confirmations | prior | 0.0609/0.5690 | 0.0149/0.0512 | 0.3679/0.9842 | N/A | 8.8285/9.4383 | 4471338.77 | 5.277 |
| standard96 | callback-w1-p100-b1024 | confirmations | public | 0.0573/0.5778 | 0.0149/0.0521 | 0.3696/0.9797 | N/A | 8.8438/9.4745 | 4465324.23 | 5.285 |
| standard96 | callback-w1-p100-b1024 | confirmations | fixed | 0.0610/0.5557 | 0.0147/0.0500 | 0.3743/0.9543 | N/A | 9.0350/9.7286 | 4432199.04 | 5.523 |
| standard96 | callback-w8-p1-b0 | initial | base | 0.0790/0.5938 | 0.0254/0.0582 | 15.4375/16.2825 | N/A | 30.7780/32.8393 | 13063.30 | 6.008 |
| standard96 | callback-w8-p1-b0 | initial | prior | 0.0717/0.5752 | 0.0261/0.0618 | 15.3856/16.4511 | N/A | 32.3895/33.4663 | 12385.88 | 5.984 |
| standard96 | callback-w8-p1-b0 | initial | public | 0.0765/0.5822 | 0.0271/0.0609 | 15.4616/16.2627 | N/A | 32.3746/33.5245 | 12440.37 | 5.980 |
| standard96 | callback-w8-p1-b0 | initial | fixed | 0.0778/0.5910 | 0.0255/0.0623 | 15.5231/16.3717 | N/A | 32.3076/33.4896 | 12434.48 | 5.977 |
| standard96 | callback-w8-p1-b0 | confirmations | base | 0.0789/0.5964 | 0.0259/0.0594 | 15.4587/16.2012 | N/A | 31.0404/32.8725 | 12984.06 | 6.010 |
| standard96 | callback-w8-p1-b0 | confirmations | prior | 0.0789/0.5837 | 0.0260/0.0610 | 15.4694/16.4342 | N/A | 32.2870/33.5805 | 12386.20 | 5.977 |
| standard96 | callback-w8-p1-b0 | confirmations | public | 0.0754/0.5777 | 0.0266/0.0602 | 15.4379/16.3849 | N/A | 32.4446/33.4380 | 12376.79 | 5.980 |
| standard96 | callback-w8-p1-b0 | confirmations | fixed | 0.0750/0.5831 | 0.0266/0.0620 | 15.6069/16.4020 | N/A | 32.2696/33.5031 | 12464.79 | 5.973 |
| standard96 | callback-w8-p1-b1024 | initial | base | 0.0733/0.5777 | 0.0238/0.0579 | 15.4816/16.1635 | N/A | 30.5338/32.7303 | 13137.32 | 5.986 |
| standard96 | callback-w8-p1-b1024 | initial | prior | 0.0776/0.6021 | 0.0256/0.0611 | 15.5378/16.3073 | N/A | 32.0840/33.2899 | 12476.54 | 5.957 |
| standard96 | callback-w8-p1-b1024 | initial | public | 0.0741/0.5810 | 0.0252/0.0607 | 15.4642/16.3846 | N/A | 32.1521/33.5964 | 12484.65 | 5.967 |
| standard96 | callback-w8-p1-b1024 | initial | fixed | 0.0754/0.5863 | 0.0247/0.0632 | 15.6316/16.3441 | N/A | 32.2243/33.0531 | 12457.44 | 5.973 |
| standard96 | callback-w8-p1-b1024 | confirmations | base | 0.0762/0.5847 | 0.0243/0.0598 | 15.4339/16.1465 | N/A | 30.5385/32.5409 | 13159.62 | 5.973 |
| standard96 | callback-w8-p1-b1024 | confirmations | prior | 0.0781/0.5979 | 0.0259/0.0621 | 15.4562/16.2793 | N/A | 32.1502/33.2448 | 12521.24 | 5.961 |
| standard96 | callback-w8-p1-b1024 | confirmations | public | 0.0802/0.5789 | 0.0261/0.0606 | 15.5130/16.4428 | N/A | 32.3715/33.4832 | 12459.92 | 5.973 |
| standard96 | callback-w8-p1-b1024 | confirmations | fixed | 0.0751/0.5880 | 0.0252/0.0600 | 15.6197/16.3590 | N/A | 32.1588/33.2806 | 12478.42 | 5.973 |
| standard96 | callback-w8-p100-b0 | initial | base | 0.0783/0.5748 | 0.0227/0.0552 | 1.2056/1.8257 | N/A | 51.6508/54.2068 | 775768.41 | 6.344 |
| standard96 | callback-w8-p100-b0 | initial | prior | 0.0839/0.5699 | 0.0266/0.0587 | 1.2052/1.8446 | N/A | 53.1767/54.4441 | 752644.67 | 6.266 |
| standard96 | callback-w8-p100-b0 | initial | public | 0.0896/0.5736 | 0.0269/0.0577 | 1.2224/1.8306 | N/A | 53.3299/54.6294 | 749510.42 | 6.271 |
| standard96 | callback-w8-p100-b0 | initial | fixed | 0.0885/0.5400 | 0.0255/0.0571 | 1.2129/1.8567 | N/A | 52.9752/53.9520 | 754442.59 | 6.320 |
| standard96 | callback-w8-p100-b0 | confirmations | base | 0.0825/0.5806 | 0.0225/0.0565 | 1.2075/1.8486 | N/A | 51.7601/53.8912 | 775444.53 | 6.344 |
| standard96 | callback-w8-p100-b0 | confirmations | prior | 0.0845/0.5636 | 0.0270/0.0593 | 1.2286/1.8345 | N/A | 53.1445/54.3128 | 753162.82 | 6.264 |
| standard96 | callback-w8-p100-b0 | confirmations | public | 0.0831/0.5803 | 0.0266/0.0582 | 1.2151/1.8612 | N/A | 53.3312/54.6640 | 750882.29 | 6.273 |
| standard96 | callback-w8-p100-b0 | confirmations | fixed | 0.0842/0.5689 | 0.0264/0.0598 | 1.2284/1.8865 | N/A | 53.1105/54.3632 | 753510.42 | 6.314 |
| standard96 | callback-w8-p100-b1024 | initial | base | 0.0727/0.5728 | 0.0223/0.0564 | 1.2112/1.8757 | N/A | 34.2524/36.1426 | 1167189.32 | 6.332 |
| standard96 | callback-w8-p100-b1024 | initial | prior | 0.0759/0.5729 | 0.0295/0.0581 | 1.2065/1.8533 | N/A | 36.0203/37.0441 | 1112681.64 | 6.242 |
| standard96 | callback-w8-p100-b1024 | initial | public | 0.0740/0.5632 | 0.0302/0.0574 | 1.1906/1.8466 | N/A | 36.1179/36.8776 | 1112969.91 | 6.250 |
| standard96 | callback-w8-p100-b1024 | initial | fixed | 0.0793/0.5729 | 0.0269/0.0587 | 1.2300/1.8779 | N/A | 36.0124/37.2379 | 1111995.08 | 6.375 |
| standard96 | callback-w8-p100-b1024 | confirmations | base | 0.0731/0.5727 | 0.0224/0.0587 | 1.1992/1.8718 | N/A | 34.4616/36.1377 | 1162513.07 | 6.336 |
| standard96 | callback-w8-p100-b1024 | confirmations | prior | 0.0775/0.5633 | 0.0297/0.0589 | 1.2058/1.8233 | N/A | 35.9500/36.9148 | 1113003.85 | 6.242 |
| standard96 | callback-w8-p100-b1024 | confirmations | public | 0.0741/0.5671 | 0.0295/0.0597 | 1.2177/1.8473 | N/A | 36.0722/37.2679 | 1111085.39 | 6.258 |
| standard96 | callback-w8-p100-b1024 | confirmations | fixed | 0.0782/0.5705 | 0.0263/0.0590 | 1.2264/1.9015 | N/A | 36.0883/37.1183 | 1112595.61 | 6.379 |
| standard96 | callback-null-b0 | initial | base | 0.0677/0.5743 | 0.0249/0.0643 | 11.7504/12.8428 | N/A | 17.1394/18.0509 | 83120.47 | 5.922 |
| standard96 | callback-null-b0 | initial | prior | 0.0696/0.5896 | 0.0255/0.0670 | 11.7996/12.8657 | N/A | 17.3868/18.2121 | 82367.19 | 5.984 |
| standard96 | callback-null-b0 | initial | public | 0.0657/0.6008 | 0.0258/0.0662 | 11.7095/12.7141 | N/A | 17.2692/17.9964 | 82953.11 | 5.977 |
| standard96 | callback-null-b0 | initial | fixed | 0.0708/0.5782 | 0.0247/0.0639 | 11.8463/12.8005 | N/A | 17.3736/18.1635 | 82742.42 | 5.980 |
| standard96 | callback-null-b0 | confirmations | base | 0.0654/0.6068 | 0.0249/0.0635 | 11.7017/12.8021 | N/A | 17.2159/18.0915 | 82785.17 | 5.918 |
| standard96 | callback-null-b0 | confirmations | prior | 0.0685/0.5911 | 0.0258/0.0651 | 11.8047/12.8208 | N/A | 17.3973/18.1612 | 82534.46 | 5.984 |
| standard96 | callback-null-b0 | confirmations | public | 0.0688/0.5871 | 0.0258/0.0634 | 11.7322/12.7702 | N/A | 17.3804/18.1348 | 82590.58 | 5.980 |
| standard96 | callback-null-b0 | confirmations | fixed | 0.0679/0.5952 | 0.0250/0.0633 | 11.7892/12.6617 | N/A | 17.4286/17.9866 | 82647.50 | 5.980 |
| standard96 | callback-null-b1024 | initial | base | 0.0661/0.5849 | 0.0214/0.0621 | 11.6503/12.7496 | N/A | 16.5543/17.4587 | 86004.69 | 5.898 |
| standard96 | callback-null-b1024 | initial | prior | 0.0659/0.5942 | 0.0223/0.0634 | 11.7737/12.9632 | N/A | 16.8331/17.7960 | 85335.46 | 5.965 |
| standard96 | callback-null-b1024 | initial | public | 0.0670/0.5805 | 0.0226/0.0647 | 11.7316/12.6274 | N/A | 16.7150/17.5248 | 85989.72 | 5.977 |
| standard96 | callback-null-b1024 | initial | fixed | 0.0672/0.5993 | 0.0229/0.0657 | 11.7328/12.6999 | N/A | 16.7245/17.3911 | 85692.05 | 5.980 |
| standard96 | unfiltered-all-b0 | initial | base | N/A | N/A | N/A | N/A | 122.5584 block-average/N/A | 2447813.80 | N/A |
| standard96 | unfiltered-all-b0 | initial | prior | N/A | N/A | N/A | N/A | 125.0114 block-average/N/A | 2399781.04 | N/A |
| standard96 | unfiltered-all-b0 | initial | public | N/A | N/A | N/A | N/A | 124.2184 block-average/N/A | 2415103.48 | N/A |
| standard96 | unfiltered-all-b0 | initial | fixed | N/A | N/A | N/A | N/A | 124.7571 block-average/N/A | 2404673.13 | N/A |
| standard96 | unfiltered-all-b0 | confirmations | base | N/A | N/A | N/A | N/A | 122.9303 block-average/N/A | 2440407.22 | N/A |
| standard96 | unfiltered-all-b0 | confirmations | prior | N/A | N/A | N/A | N/A | 124.3326 block-average/N/A | 2412883.55 | N/A |
| standard96 | unfiltered-all-b0 | confirmations | public | N/A | N/A | N/A | N/A | 123.9374 block-average/N/A | 2420577.34 | N/A |
| standard96 | unfiltered-all-b0 | confirmations | fixed | N/A | N/A | N/A | N/A | 124.7805 block-average/N/A | 2404222.78 | N/A |
| standard96 | unfiltered-all-b1024 | initial | base | N/A | N/A | N/A | N/A | 19.8447 block-average/N/A | 15117435.68 | N/A |
| standard96 | unfiltered-all-b1024 | initial | prior | N/A | N/A | N/A | N/A | 19.8191 block-average/N/A | 15137022.58 | N/A |
| standard96 | unfiltered-all-b1024 | initial | public | N/A | N/A | N/A | N/A | 19.8503 block-average/N/A | 15113112.34 | N/A |
| standard96 | unfiltered-all-b1024 | initial | fixed | N/A | N/A | N/A | N/A | 19.9019 block-average/N/A | 15073923.54 | N/A |
| standard96 | unfiltered-time-b0 | initial | base | N/A | N/A | N/A | N/A | 82.4458 block-average/N/A | 2425837.09 | N/A |
| standard96 | unfiltered-time-b0 | initial | prior | N/A | N/A | N/A | N/A | 82.8680 block-average/N/A | 2413478.07 | N/A |
| standard96 | unfiltered-time-b0 | initial | public | N/A | N/A | N/A | N/A | 82.9256 block-average/N/A | 2411801.09 | N/A |
| standard96 | unfiltered-time-b0 | initial | fixed | N/A | N/A | N/A | N/A | 83.7384 block-average/N/A | 2388394.36 | N/A |
| standard96 | unfiltered-time-b0 | confirmations | base | N/A | N/A | N/A | N/A | 82.1038 block-average/N/A | 2435940.67 | N/A |
| standard96 | unfiltered-time-b0 | confirmations | prior | N/A | N/A | N/A | N/A | 83.0269 block-average/N/A | 2408858.51 | N/A |
| standard96 | unfiltered-time-b0 | confirmations | public | N/A | N/A | N/A | N/A | 83.0066 block-average/N/A | 2409446.66 | N/A |
| standard96 | unfiltered-time-b0 | confirmations | fixed | N/A | N/A | N/A | N/A | 83.6097 block-average/N/A | 2392069.82 | N/A |
| standard96 | unfiltered-time-b1024 | initial | base | N/A | N/A | N/A | N/A | 13.4914 block-average/N/A | 14824344.09 | N/A |
| standard96 | unfiltered-time-b1024 | initial | prior | N/A | N/A | N/A | N/A | 13.4336 block-average/N/A | 14888021.62 | N/A |
| standard96 | unfiltered-time-b1024 | initial | public | N/A | N/A | N/A | N/A | 13.2879 block-average/N/A | 15051331.33 | N/A |
| standard96 | unfiltered-time-b1024 | initial | fixed | N/A | N/A | N/A | N/A | 13.4659 block-average/N/A | 14852296.20 | N/A |
| standard96 | unfiltered-offset-b0 | initial | base | N/A | N/A | N/A | N/A | 36.6685 block-average/N/A | 1784419.00 | N/A |
| standard96 | unfiltered-offset-b0 | initial | prior | N/A | N/A | N/A | N/A | 37.6185 block-average/N/A | 1739358.57 | N/A |
| standard96 | unfiltered-offset-b0 | initial | public | N/A | N/A | N/A | N/A | 37.1119 block-average/N/A | 1763100.29 | N/A |
| standard96 | unfiltered-offset-b0 | initial | fixed | N/A | N/A | N/A | N/A | 37.5909 block-average/N/A | 1740638.52 | N/A |
| standard96 | unfiltered-offset-b0 | confirmations | base | N/A | N/A | N/A | N/A | 36.8505 block-average/N/A | 1775606.85 | N/A |
| standard96 | unfiltered-offset-b0 | confirmations | prior | N/A | N/A | N/A | N/A | 37.2146 block-average/N/A | 1758236.01 | N/A |
| standard96 | unfiltered-offset-b0 | confirmations | public | N/A | N/A | N/A | N/A | 37.3427 block-average/N/A | 1752203.01 | N/A |
| standard96 | unfiltered-offset-b0 | confirmations | fixed | N/A | N/A | N/A | N/A | 37.2595 block-average/N/A | 1756114.79 | N/A |
| standard96 | unfiltered-offset-b1024 | initial | base | N/A | N/A | N/A | N/A | 14.0219 block-average/N/A | 4666413.38 | N/A |
| standard96 | unfiltered-offset-b1024 | initial | prior | N/A | N/A | N/A | N/A | 13.9533 block-average/N/A | 4689383.98 | N/A |
| standard96 | unfiltered-offset-b1024 | initial | public | N/A | N/A | N/A | N/A | 13.8114 block-average/N/A | 4737542.39 | N/A |
| standard96 | unfiltered-offset-b1024 | initial | fixed | N/A | N/A | N/A | N/A | 13.7675 block-average/N/A | 4752753.94 | N/A |
| standard96 | unfiltered-sparse-b0 | initial | base | N/A | N/A | N/A | N/A | 163.8379 block-average/N/A | 1831078.45 | N/A |
| standard96 | unfiltered-sparse-b0 | initial | prior | N/A | N/A | N/A | N/A | 164.8689 block-average/N/A | 1819628.31 | N/A |
| standard96 | unfiltered-sparse-b0 | initial | public | N/A | N/A | N/A | N/A | 164.2969 block-average/N/A | 1825962.50 | N/A |
| standard96 | unfiltered-sparse-b0 | initial | fixed | N/A | N/A | N/A | N/A | 165.1184 block-average/N/A | 1816878.46 | N/A |
| standard96 | unfiltered-sparse-b0 | confirmations | base | N/A | N/A | N/A | N/A | 163.5947 block-average/N/A | 1833800.19 | N/A |
| standard96 | unfiltered-sparse-b0 | confirmations | prior | N/A | N/A | N/A | N/A | 164.8953 block-average/N/A | 1819336.77 | N/A |
| standard96 | unfiltered-sparse-b0 | confirmations | public | N/A | N/A | N/A | N/A | 164.4821 block-average/N/A | 1823906.47 | N/A |
| standard96 | unfiltered-sparse-b0 | confirmations | fixed | N/A | N/A | N/A | N/A | 164.7468 block-average/N/A | 1820975.67 | N/A |
| standard96 | unfiltered-sparse-b1024 | initial | base | N/A | N/A | N/A | N/A | 60.8078 block-average/N/A | 4933579.60 | N/A |
| standard96 | unfiltered-sparse-b1024 | initial | prior | N/A | N/A | N/A | N/A | 61.2279 block-average/N/A | 4899729.51 | N/A |
| standard96 | unfiltered-sparse-b1024 | initial | public | N/A | N/A | N/A | N/A | 60.9487 block-average/N/A | 4922176.26 | N/A |
| standard96 | unfiltered-sparse-b1024 | initial | fixed | N/A | N/A | N/A | N/A | 61.0941 block-average/N/A | 4910454.92 | N/A |
| standard96 | unfiltered-sparse-b1024 | confirmations | base | N/A | N/A | N/A | N/A | 60.4928 block-average/N/A | 4959271.78 | N/A |
| standard96 | unfiltered-sparse-b1024 | confirmations | prior | N/A | N/A | N/A | N/A | 60.7094 block-average/N/A | 4941570.20 | N/A |
| standard96 | unfiltered-sparse-b1024 | confirmations | public | N/A | N/A | N/A | N/A | 60.4214 block-average/N/A | 4965132.32 | N/A |
| standard96 | unfiltered-sparse-b1024 | confirmations | fixed | N/A | N/A | N/A | N/A | 60.3734 block-average/N/A | 4969077.37 | N/A |
| standard96 | float-not-t0-mixed0-cut0-b0 | initial | base | 0.0614/0.5768 | 0.0152/0.0473 | 0.3438/0.9634 | N/A | 11.3459/11.7489 | 3549330.22 | 5.617 |
| standard96 | float-not-t0-mixed0-cut0-b0 | initial | prior | 0.0542/0.5871 | 0.0146/0.0601 | 0.5825/1.2420 | N/A | 5.4505/6.1661 | 7085114.27 | 5.617 |
| standard96 | float-not-t0-mixed0-cut0-b0 | initial | public | 0.0522/0.5738 | 0.0172/0.0585 | 0.5801/1.2202 | N/A | 5.4478/6.1136 | 7123756.21 | 5.635 |
| standard96 | float-not-t0-mixed0-cut0-b0 | initial | fixed | 0.0524/0.5870 | 0.0175/0.0590 | 0.5887/1.2439 | N/A | 5.4532/6.1425 | 7114194.28 | 5.645 |
| standard96 | float-not-t0-mixed0-cut0-b1024 | initial | base | 0.0567/0.6001 | 0.0151/0.0505 | 0.3335/0.9733 | N/A | 7.9229/8.4832 | 5001241.43 | 5.273 |
| standard96 | float-not-t0-mixed0-cut0-b1024 | initial | prior | 0.0517/0.5765 | 0.0152/0.0586 | 0.5769/1.2494 | N/A | 2.2807/3.0090 | 16226302.98 | 5.691 |
| standard96 | float-not-t0-mixed0-cut0-b1024 | initial | public | 0.0589/0.5691 | 0.0155/0.0611 | 0.5866/1.2550 | N/A | 2.2826/3.1608 | 16155766.13 | 5.703 |
| standard96 | float-not-t0-mixed0-cut0-b1024 | initial | fixed | 0.0505/0.5591 | 0.0158/0.0605 | 0.5727/1.2150 | N/A | 2.2675/2.9946 | 16264728.38 | 5.711 |
| standard96 | float-not-t0-mixed0-cut50-b0 | initial | base | 0.0602/0.5466 | 0.0130/0.0440 | 0.5073/1.0853 | N/A | 8.9093/9.4676 | 2218455.28 | 5.109 |
| standard96 | float-not-t0-mixed0-cut50-b0 | initial | prior | 0.0479/0.5401 | 0.0147/0.0545 | 0.6856/1.3028 | N/A | 4.1496/4.8117 | 4598706.10 | 5.273 |
| standard96 | float-not-t0-mixed0-cut50-b0 | initial | public | 0.0478/0.5487 | 0.0139/0.0522 | 0.6517/1.2418 | N/A | 4.0020/4.6742 | 4791458.30 | 5.342 |
| standard96 | float-not-t0-mixed0-cut50-b0 | initial | fixed | 0.0476/0.5439 | 0.0136/0.0552 | 0.6498/1.2775 | N/A | 4.0220/4.6973 | 4772197.20 | 5.301 |
| standard96 | float-not-t0-mixed0-cut50-b1024 | initial | base | 0.0605/0.5545 | 0.0131/0.0443 | 0.5013/1.0696 | N/A | 7.3042/8.0440 | 2691266.29 | 5.164 |
| standard96 | float-not-t0-mixed0-cut50-b1024 | initial | prior | 0.0465/0.5278 | 0.0138/0.0523 | 0.6828/1.2774 | N/A | 2.5677/3.2135 | 7262790.98 | 5.324 |
| standard96 | float-not-t0-mixed0-cut50-b1024 | initial | public | 0.0460/0.5347 | 0.0140/0.0549 | 0.6401/1.2414 | N/A | 2.4202/3.0744 | 7704267.71 | 5.383 |
| standard96 | float-not-t0-mixed0-cut50-b1024 | initial | fixed | 0.0461/0.5531 | 0.0140/0.0542 | 0.6366/1.2543 | N/A | 2.4051/3.1125 | 7718431.65 | 5.395 |
| standard96 | float-not-t0-mixed0-cut100-b0 | initial | base | 0.0522/0.5542 | 0.0123/0.0437 | N/A | N/A | 6.9657/7.8732 | 0.00 | 4.955 |
| standard96 | float-not-t0-mixed0-cut100-b0 | initial | prior | 0.0421/0.5357 | 0.0103/0.0559 | N/A | N/A | 0.4464/1.0799 | 0.00 | 4.945 |
| standard96 | float-not-t0-mixed0-cut100-b0 | initial | public | 0.0418/0.5552 | 0.0106/0.0569 | N/A | N/A | 0.4325/1.1053 | 0.00 | 4.934 |
| standard96 | float-not-t0-mixed0-cut100-b0 | initial | fixed | 0.0422/0.5612 | 0.0106/0.0575 | N/A | N/A | 0.4354/1.1136 | 0.00 | 4.938 |
| standard96 | float-not-t0-mixed0-cut100-b1024 | initial | base | 0.0482/0.5428 | 0.0109/0.0434 | N/A | N/A | 6.9233/7.4459 | 0.00 | 4.945 |
| standard96 | float-not-t0-mixed0-cut100-b1024 | initial | prior | 0.0420/0.5513 | 0.0101/0.0562 | N/A | N/A | 0.4423/1.0920 | 0.00 | 4.945 |
| standard96 | float-not-t0-mixed0-cut100-b1024 | initial | public | 0.0418/0.5497 | 0.0105/0.0597 | N/A | N/A | 0.4354/1.1110 | 0.00 | 4.932 |
| standard96 | float-not-t0-mixed0-cut100-b1024 | initial | fixed | 0.0420/0.5394 | 0.0104/0.0569 | N/A | N/A | 0.4335/1.0850 | 0.00 | 4.941 |
| standard96 | float-not-t0-mixed1-cut0-b0 | initial | base | 0.0610/0.5582 | 0.0150/0.0466 | 0.3622/0.9473 | N/A | 11.4459/11.7883 | 3337718.87 | 5.598 |
| standard96 | float-not-t0-mixed1-cut0-b0 | initial | prior | 0.0628/0.5577 | 0.0168/0.0566 | 0.3799/0.9691 | N/A | 11.8152/12.1192 | 3238204.67 | 5.621 |
| standard96 | float-not-t0-mixed1-cut0-b0 | initial | public | 0.0529/0.5443 | 0.0164/0.0564 | 0.7179/1.3282 | N/A | 5.8186/6.5035 | 6317175.81 | 5.631 |
| standard96 | float-not-t0-mixed1-cut0-b0 | initial | fixed | 0.0510/0.5656 | 0.0158/0.0570 | 0.7173/1.3511 | N/A | 5.8443/6.5172 | 6329785.76 | 5.637 |
| standard96 | float-not-t0-mixed1-cut0-b1024 | initial | base | 0.0560/0.5529 | 0.0130/0.0445 | 0.3429/0.9544 | N/A | 8.0708/8.6121 | 4665801.22 | 5.250 |
| standard96 | float-not-t0-mixed1-cut0-b1024 | initial | prior | 0.0491/0.5246 | 0.0137/0.0512 | 0.3509/0.9183 | N/A | 8.3603/8.9350 | 4455697.59 | 5.422 |
| standard96 | float-not-t0-mixed1-cut0-b1024 | initial | public | 0.0481/0.5302 | 0.0146/0.0553 | 0.6932/1.3309 | N/A | 2.7725/3.4723 | 12768310.72 | 5.688 |
| standard96 | float-not-t0-mixed1-cut0-b1024 | initial | fixed | 0.0489/0.5401 | 0.0143/0.0545 | 0.6872/1.3254 | N/A | 2.7443/3.4733 | 12834258.22 | 5.695 |
| standard96 | float-not-t0-mixed1-cut50-b0 | initial | base | 0.0608/0.5480 | 0.0136/0.0447 | 0.5462/1.1160 | N/A | 9.1515/9.7586 | 2064785.12 | 5.102 |
| standard96 | float-not-t0-mixed1-cut50-b0 | initial | prior | 0.0581/0.5341 | 0.0152/0.0487 | 0.5653/1.1214 | N/A | 9.4908/10.0239 | 2001795.50 | 5.182 |
| standard96 | float-not-t0-mixed1-cut50-b0 | initial | public | 0.0505/0.5484 | 0.0136/0.0546 | 0.6494/1.2611 | N/A | 3.9664/4.6028 | 4633187.18 | 5.332 |
| standard96 | float-not-t0-mixed1-cut50-b0 | initial | fixed | 0.0478/0.5526 | 0.0135/0.0566 | 0.6580/1.2943 | N/A | 3.9705/4.6256 | 4608809.25 | 5.285 |
| standard96 | float-not-t0-mixed1-cut50-b1024 | initial | base | 0.0563/0.5376 | 0.0120/0.0445 | 0.5532/1.0893 | N/A | 7.7930/8.3874 | 2449172.95 | 5.158 |
| standard96 | float-not-t0-mixed1-cut50-b1024 | initial | prior | 0.0519/0.5431 | 0.0123/0.0492 | 0.5610/1.1304 | N/A | 8.0425/8.5676 | 2358998.13 | 5.182 |
| standard96 | float-not-t0-mixed1-cut50-b1024 | initial | public | 0.0472/0.5579 | 0.0137/0.0554 | 0.6504/1.2736 | N/A | 2.4446/3.1281 | 7266573.25 | 5.383 |
| standard96 | float-not-t0-mixed1-cut50-b1024 | initial | fixed | 0.0465/0.5470 | 0.0131/0.0548 | 0.6477/1.2588 | N/A | 2.4462/3.1070 | 7270620.32 | 5.391 |
| standard96 | float-not-t0-mixed1-cut100-b0 | initial | base | 0.0507/0.5360 | 0.0132/0.0442 | 3.6117/4.2442 | N/A | 7.1584/8.0324 | 53813.15 | 4.955 |
| standard96 | float-not-t0-mixed1-cut100-b0 | initial | prior | 0.0502/0.5490 | 0.0139/0.0539 | 3.7737/4.3633 | N/A | 7.5412/8.1531 | 51050.92 | 4.980 |
| standard96 | float-not-t0-mixed1-cut100-b0 | initial | public | 0.0483/0.5502 | 0.0132/0.0568 | 1.0172/1.6629 | N/A | 2.0238/2.6898 | 176987.25 | 5.035 |
| standard96 | float-not-t0-mixed1-cut100-b0 | initial | fixed | 0.0467/0.5536 | 0.0131/0.0565 | 1.0146/1.6610 | N/A | 2.0215/2.6788 | 177477.49 | 5.043 |
| standard96 | float-not-t0-mixed1-cut100-b1024 | initial | base | 0.0609/0.5646 | 0.0121/0.0459 | 3.6324/4.3687 | N/A | 7.1806/8.1541 | 53640.01 | 4.951 |
| standard96 | float-not-t0-mixed1-cut100-b1024 | initial | prior | 0.0558/0.5564 | 0.0123/0.0523 | 3.7978/4.3735 | N/A | 7.5674/8.2711 | 51137.26 | 4.979 |
| standard96 | float-not-t0-mixed1-cut100-b1024 | initial | public | 0.0469/0.5780 | 0.0124/0.0584 | 1.0169/1.6989 | N/A | 1.9980/2.7019 | 178149.44 | 5.033 |
| standard96 | float-not-t0-mixed1-cut100-b1024 | initial | fixed | 0.0500/0.5685 | 0.0123/0.0593 | 1.0243/1.6860 | N/A | 2.0063/2.7362 | 178707.17 | 5.041 |
| standard96 | float-not-t1-mixed0-cut0-b0 | initial | base | 0.0613/0.5588 | 0.0132/0.0457 | 0.3339/0.9235 | N/A | 10.8673/11.3315 | 3682041.08 | 5.271 |
| standard96 | float-not-t1-mixed0-cut0-b0 | initial | prior | 0.0502/0.5633 | 0.0146/0.0554 | 0.5792/1.2117 | N/A | 5.1791/5.8940 | 7469542.70 | 5.719 |
| standard96 | float-not-t1-mixed0-cut0-b0 | initial | public | 0.0561/0.5658 | 0.0142/0.0571 | 0.5885/1.2131 | N/A | 5.2043/5.9006 | 7438908.55 | 5.723 |
| standard96 | float-not-t1-mixed0-cut0-b0 | initial | fixed | 0.0525/0.5491 | 0.0146/0.0614 | 0.5989/1.2297 | N/A | 5.2537/5.9645 | 7390054.05 | 5.727 |
| standard96 | float-not-t1-mixed0-cut0-b0 | confirmations | base | 0.0582/0.5818 | 0.0132/0.0457 | 0.3295/0.9419 | N/A | 10.9248/11.3246 | 3675243.71 | 5.561 |
| standard96 | float-not-t1-mixed0-cut0-b0 | confirmations | prior | 0.0493/0.5824 | 0.0134/0.0558 | 0.5777/1.2498 | N/A | 5.2001/5.9228 | 7434003.69 | 5.715 |
| standard96 | float-not-t1-mixed0-cut0-b0 | confirmations | public | 0.0507/0.5690 | 0.0144/0.0563 | 0.5834/1.2309 | N/A | 5.1958/5.9087 | 7435543.49 | 5.721 |
| standard96 | float-not-t1-mixed0-cut0-b0 | confirmations | fixed | 0.0500/0.5640 | 0.0146/0.0570 | 0.5925/1.2207 | N/A | 5.2405/5.9499 | 7413722.80 | 5.727 |
| standard96 | float-not-t1-mixed0-cut0-b1024 | initial | base | 0.0516/0.5406 | 0.0122/0.0456 | 0.3155/0.9086 | N/A | 7.7340/8.3085 | 5112564.98 | 5.264 |
| standard96 | float-not-t1-mixed0-cut0-b1024 | initial | prior | 0.0479/0.5613 | 0.0120/0.0556 | 0.5695/1.2125 | N/A | 2.2714/2.9890 | 16263910.23 | 5.781 |
| standard96 | float-not-t1-mixed0-cut0-b1024 | initial | public | 0.0469/0.5219 | 0.0123/0.0559 | 0.5698/1.1783 | N/A | 2.2385/2.9540 | 16403190.83 | 5.789 |
| standard96 | float-not-t1-mixed0-cut0-b1024 | initial | fixed | 0.0481/0.5349 | 0.0129/0.0556 | 0.5758/1.1911 | N/A | 2.2582/2.9758 | 16279580.63 | 5.797 |
| standard96 | float-not-t1-mixed0-cut50-b0 | initial | base | 0.0525/0.5507 | 0.0129/0.0445 | 0.4939/1.0660 | N/A | 8.6933/9.3082 | 2277498.37 | 5.113 |
| standard96 | float-not-t1-mixed0-cut50-b0 | initial | prior | 0.0483/0.5333 | 0.0148/0.0548 | 0.7029/1.3265 | N/A | 4.0853/4.7892 | 4680351.51 | 5.309 |
| standard96 | float-not-t1-mixed0-cut50-b0 | initial | public | 0.0509/0.5320 | 0.0143/0.0533 | 0.6623/1.2541 | N/A | 3.9015/4.5696 | 4902261.85 | 5.371 |
| standard96 | float-not-t1-mixed0-cut50-b0 | initial | fixed | 0.0502/0.5479 | 0.0140/0.0560 | 0.6636/1.3033 | N/A | 3.9311/4.6619 | 4865080.32 | 5.330 |
| standard96 | float-not-t1-mixed0-cut50-b0 | confirmations | base | 0.0601/0.5684 | 0.0137/0.0449 | 0.5007/1.1099 | N/A | 8.7366/9.3682 | 2262994.06 | 5.113 |
| standard96 | float-not-t1-mixed0-cut50-b0 | confirmations | prior | 0.0498/0.5603 | 0.0150/0.0557 | 0.7095/1.3359 | N/A | 4.1142/4.8014 | 4658330.96 | 5.309 |
| standard96 | float-not-t1-mixed0-cut50-b0 | confirmations | public | 0.0488/0.5488 | 0.0145/0.0529 | 0.6668/1.2571 | N/A | 3.9114/4.5883 | 4894463.29 | 5.371 |
| standard96 | float-not-t1-mixed0-cut50-b0 | confirmations | fixed | 0.0486/0.5485 | 0.0140/0.0570 | 0.6668/1.3003 | N/A | 3.9505/4.6481 | 4843005.98 | 5.332 |
| standard96 | float-not-t1-mixed0-cut50-b1024 | initial | base | 0.0501/0.5518 | 0.0129/0.0444 | 0.5000/1.0648 | N/A | 7.3424/7.9178 | 2701616.32 | 5.164 |
| standard96 | float-not-t1-mixed0-cut50-b1024 | initial | prior | 0.0471/0.5292 | 0.0132/0.0528 | 0.7061/1.2827 | N/A | 2.6368/3.3209 | 7076813.09 | 5.352 |
| standard96 | float-not-t1-mixed0-cut50-b1024 | initial | public | 0.0474/0.5176 | 0.0128/0.0548 | 0.6599/1.2383 | N/A | 2.4830/3.1094 | 7557821.62 | 5.371 |
| standard96 | float-not-t1-mixed0-cut50-b1024 | initial | fixed | 0.0475/0.5634 | 0.0136/0.0531 | 0.6622/1.2767 | N/A | 2.4728/3.1529 | 7539772.98 | 5.383 |
| standard96 | float-not-t1-mixed0-cut100-b0 | initial | base | 0.0543/0.5570 | 0.0126/0.0455 | N/A | N/A | 6.9640/7.7416 | 0.00 | 4.941 |
| standard96 | float-not-t1-mixed0-cut100-b0 | initial | prior | 0.0429/0.5728 | 0.0111/0.0587 | N/A | N/A | 0.4951/1.1772 | 0.00 | 4.906 |
| standard96 | float-not-t1-mixed0-cut100-b0 | initial | public | 0.0426/0.5660 | 0.0108/0.0574 | N/A | N/A | 0.4865/1.2021 | 0.00 | 4.906 |
| standard96 | float-not-t1-mixed0-cut100-b0 | initial | fixed | 0.0435/0.5653 | 0.0111/0.0579 | N/A | N/A | 0.4859/1.1710 | 0.00 | 4.914 |
| standard96 | float-not-t1-mixed0-cut100-b1024 | initial | base | 0.0504/0.5348 | 0.0125/0.0433 | N/A | N/A | 6.8253/7.4064 | 0.00 | 4.945 |
| standard96 | float-not-t1-mixed0-cut100-b1024 | initial | prior | 0.0423/0.5187 | 0.0126/0.0551 | N/A | N/A | 0.4952/1.1102 | 0.00 | 4.906 |
| standard96 | float-not-t1-mixed0-cut100-b1024 | initial | public | 0.0420/0.5330 | 0.0123/0.0556 | N/A | N/A | 0.4846/1.1273 | 0.00 | 4.906 |
| standard96 | float-not-t1-mixed0-cut100-b1024 | initial | fixed | 0.0425/0.5398 | 0.0123/0.0561 | N/A | N/A | 0.4825/1.1250 | 0.00 | 4.914 |
| standard96 | float-not-t1-mixed1-cut0-b0 | initial | base | 0.0611/0.5485 | 0.0141/0.0457 | 0.3537/0.9232 | N/A | 11.0503/11.4535 | 3465335.05 | 5.412 |
| standard96 | float-not-t1-mixed1-cut0-b0 | initial | prior | 0.0611/0.5515 | 0.0150/0.0515 | 0.3637/0.9483 | N/A | 11.3329/11.5796 | 3363850.57 | 5.617 |
| standard96 | float-not-t1-mixed1-cut0-b0 | initial | public | 0.0501/0.5566 | 0.0154/0.0563 | 0.7453/1.3626 | N/A | 5.6577/6.3870 | 6497247.47 | 5.699 |
| standard96 | float-not-t1-mixed1-cut0-b0 | initial | fixed | 0.0521/0.5686 | 0.0151/0.0563 | 0.7355/1.3689 | N/A | 5.7045/6.4518 | 6451671.52 | 5.711 |
| standard96 | float-not-t1-mixed1-cut0-b1024 | initial | base | 0.0592/0.5589 | 0.0132/0.0460 | 0.3497/0.9448 | N/A | 8.1693/8.7976 | 4647940.73 | 5.246 |
| standard96 | float-not-t1-mixed1-cut0-b1024 | initial | prior | 0.0606/0.5445 | 0.0133/0.0518 | 0.3519/0.9266 | N/A | 8.2361/8.8479 | 4537968.38 | 5.410 |
| standard96 | float-not-t1-mixed1-cut0-b1024 | initial | public | 0.0488/0.5553 | 0.0138/0.0560 | 0.7227/1.3586 | N/A | 2.8945/3.6449 | 12298921.63 | 5.773 |
| standard96 | float-not-t1-mixed1-cut0-b1024 | initial | fixed | 0.0498/0.5594 | 0.0132/0.0568 | 0.7236/1.3708 | N/A | 2.8797/3.6081 | 12348022.54 | 5.781 |
| standard96 | float-not-t1-mixed1-cut50-b0 | initial | base | 0.0602/0.5566 | 0.0132/0.0460 | 0.5341/1.1247 | N/A | 8.9354/9.4627 | 2116129.23 | 5.105 |
| standard96 | float-not-t1-mixed1-cut50-b0 | initial | prior | 0.0609/0.5374 | 0.0142/0.0495 | 0.5548/1.0993 | N/A | 9.2245/9.7303 | 2060895.20 | 5.188 |
| standard96 | float-not-t1-mixed1-cut50-b0 | initial | public | 0.0503/0.5690 | 0.0143/0.0533 | 0.6745/1.2824 | N/A | 3.9025/4.5661 | 4700046.85 | 5.355 |
| standard96 | float-not-t1-mixed1-cut50-b0 | initial | fixed | 0.0485/0.5645 | 0.0137/0.0568 | 0.6703/1.3254 | N/A | 3.9315/4.6676 | 4646082.87 | 5.309 |
| standard96 | float-not-t1-mixed1-cut50-b0 | confirmations | base | 0.0573/0.5781 | 0.0144/0.0468 | 0.5352/1.1420 | N/A | 8.9167/9.6509 | 2118033.78 | 5.105 |
| standard96 | float-not-t1-mixed1-cut50-b0 | confirmations | prior | 0.0536/0.5650 | 0.0149/0.0501 | 0.5452/1.1306 | N/A | 9.1877/9.7711 | 2057146.55 | 5.188 |
| standard96 | float-not-t1-mixed1-cut50-b0 | confirmations | public | 0.0505/0.5611 | 0.0153/0.0571 | 0.6708/1.2940 | N/A | 3.9062/4.5974 | 4683332.66 | 5.355 |
| standard96 | float-not-t1-mixed1-cut50-b0 | confirmations | fixed | 0.0500/0.5580 | 0.0149/0.0579 | 0.6771/1.3208 | N/A | 3.9322/4.6326 | 4645124.16 | 5.309 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | initial | base | 0.0482/0.5339 | 0.0126/0.0430 | 0.5229/1.0765 | N/A | 7.4691/8.0966 | 2518173.13 | 5.164 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | initial | prior | 0.0482/0.5214 | 0.0139/0.0484 | 0.5337/1.0858 | N/A | 7.7544/8.3192 | 2433551.80 | 5.188 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | initial | public | 0.0462/0.5357 | 0.0131/0.0532 | 0.6618/1.2442 | N/A | 2.5055/3.1210 | 7120184.37 | 5.359 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | initial | fixed | 0.0470/0.5396 | 0.0132/0.0534 | 0.6709/1.2614 | N/A | 2.5106/3.1505 | 7081807.24 | 5.367 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | confirmations | base | 0.0494/0.5433 | 0.0126/0.0444 | 0.5259/1.0904 | N/A | 7.5673/8.1295 | 2507030.55 | 5.162 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | confirmations | prior | 0.0519/0.5445 | 0.0141/0.0487 | 0.5458/1.1090 | N/A | 7.8485/8.3927 | 2421522.98 | 5.191 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | confirmations | public | 0.0476/0.5380 | 0.0137/0.0545 | 0.6668/1.2637 | N/A | 2.5114/3.1602 | 7107579.58 | 5.357 |
| standard96 | float-not-t1-mixed1-cut50-b1024 | confirmations | fixed | 0.0473/0.5344 | 0.0136/0.0533 | 0.6697/1.2622 | N/A | 2.5151/3.1697 | 7077358.56 | 5.365 |
| standard96 | float-not-t1-mixed1-cut100-b0 | initial | base | 0.0480/0.5360 | 0.0141/0.0436 | 3.5213/4.0809 | N/A | 7.0261/7.5941 | 54862.53 | 4.949 |
| standard96 | float-not-t1-mixed1-cut100-b0 | initial | prior | 0.0503/0.5548 | 0.0132/0.0524 | 3.6664/4.2749 | N/A | 7.3256/7.9743 | 52537.41 | 4.977 |
| standard96 | float-not-t1-mixed1-cut100-b0 | initial | public | 0.0476/0.5554 | 0.0134/0.0565 | 1.0459/1.7051 | N/A | 2.0685/2.7551 | 173043.00 | 5.037 |
| standard96 | float-not-t1-mixed1-cut100-b0 | initial | fixed | 0.0472/0.5519 | 0.0130/0.0572 | 1.0451/1.6981 | N/A | 2.0810/2.7598 | 172039.57 | 5.062 |
| standard96 | float-not-t1-mixed1-cut100-b1024 | initial | base | 0.0529/0.5597 | 0.0123/0.0472 | 3.6099/4.3496 | N/A | 7.1006/8.0537 | 54265.97 | 4.953 |
| standard96 | float-not-t1-mixed1-cut100-b1024 | initial | prior | 0.0519/0.5658 | 0.0123/0.0537 | 3.6536/4.3400 | N/A | 7.2945/8.0470 | 52492.75 | 4.979 |
| standard96 | float-not-t1-mixed1-cut100-b1024 | initial | public | 0.0477/0.5786 | 0.0128/0.0587 | 1.0627/1.7329 | N/A | 2.0852/2.7917 | 171618.72 | 5.098 |
| standard96 | float-not-t1-mixed1-cut100-b1024 | initial | fixed | 0.0484/0.5472 | 0.0132/0.0573 | 1.0595/1.7124 | N/A | 2.0799/2.7714 | 172356.95 | 5.107 |
| standard96 | float-callback-t0-cut0-b0 | initial | base | 0.0614/0.5544 | 0.0128/0.0478 | 0.3539/0.9642 | N/A | 11.4659/11.9363 | 3334942.09 | 5.602 |
| standard96 | float-callback-t0-cut0-b0 | initial | prior | 0.0607/0.5488 | 0.0152/0.0522 | 0.3643/0.9496 | N/A | 11.8194/12.1180 | 3230506.41 | 5.623 |
| standard96 | float-callback-t0-cut0-b0 | initial | public | 0.0612/0.5521 | 0.0147/0.0521 | 0.3807/0.9619 | N/A | 11.6620/12.5326 | 3279245.83 | 5.660 |
| standard96 | float-callback-t0-cut0-b0 | initial | fixed | 0.0610/0.5731 | 0.0150/0.0559 | 0.3662/0.9913 | N/A | 11.5440/12.0773 | 3308927.25 | 5.645 |
| standard96 | float-callback-t0-cut0-b1024 | initial | base | 0.0607/0.5656 | 0.0137/0.0466 | 0.3482/0.9641 | N/A | 8.1040/8.7987 | 4607509.43 | 5.250 |
| standard96 | float-callback-t0-cut0-b1024 | initial | prior | 0.0608/0.5584 | 0.0165/0.0524 | 0.3718/0.9569 | N/A | 8.5184/9.0424 | 4405152.81 | 5.422 |
| standard96 | float-callback-t0-cut0-b1024 | initial | public | 0.0542/0.5671 | 0.0156/0.0529 | 0.3676/0.9606 | N/A | 8.5969/9.3823 | 4471357.93 | 5.430 |
| standard96 | float-callback-t0-cut0-b1024 | initial | fixed | 0.0611/0.5933 | 0.0158/0.0547 | 0.3649/0.9932 | N/A | 8.3581/8.9064 | 4511199.62 | 5.430 |
| standard96 | float-callback-t0-cut0-b1024 | confirmations | base | 0.0532/0.5745 | 0.0127/0.0467 | 0.3433/0.9550 | N/A | 8.1041/8.8473 | 4607654.96 | 5.250 |
| standard96 | float-callback-t0-cut0-b1024 | confirmations | prior | 0.0565/0.5693 | 0.0146/0.0526 | 0.3670/0.9705 | N/A | 8.4417/9.0491 | 4423510.87 | 5.422 |
| standard96 | float-callback-t0-cut0-b1024 | confirmations | public | 0.0520/0.5620 | 0.0150/0.0512 | 0.3717/0.9590 | N/A | 8.5991/9.2995 | 4490003.69 | 5.426 |
| standard96 | float-callback-t0-cut0-b1024 | confirmations | fixed | 0.0510/0.5507 | 0.0144/0.0522 | 0.3572/0.9504 | N/A | 8.2321/8.8689 | 4538865.69 | 5.430 |
| standard96 | float-callback-t0-cut50-b0 | initial | base | 0.0602/0.5548 | 0.0135/0.0468 | 0.5409/1.1255 | N/A | 9.2044/9.8898 | 2065950.72 | 5.102 |
| standard96 | float-callback-t0-cut50-b0 | initial | prior | 0.0601/0.5655 | 0.0149/0.0499 | 0.5683/1.1458 | N/A | 9.4764/10.2788 | 1993750.18 | 5.184 |
| standard96 | float-callback-t0-cut50-b0 | initial | public | 0.0600/0.5460 | 0.0162/0.0506 | 0.5685/1.1302 | N/A | 9.5505/10.2869 | 2031851.63 | 5.191 |
| standard96 | float-callback-t0-cut50-b0 | initial | fixed | 0.0563/0.5474 | 0.0140/0.0493 | 0.5497/1.1286 | N/A | 9.3507/10.0009 | 2029523.88 | 5.199 |
| standard96 | float-callback-t0-cut50-b0 | confirmations | base | 0.0536/0.5451 | 0.0127/0.0455 | 0.5452/1.1245 | N/A | 9.1559/9.8002 | 2065630.79 | 5.102 |
| standard96 | float-callback-t0-cut50-b0 | confirmations | prior | 0.0544/0.5454 | 0.0138/0.0502 | 0.5607/1.1179 | N/A | 9.5092/10.0557 | 1992961.13 | 5.184 |
| standard96 | float-callback-t0-cut50-b0 | confirmations | public | 0.0610/0.5406 | 0.0152/0.0504 | 0.5676/1.1539 | N/A | 9.6286/10.3617 | 2012551.44 | 5.191 |
| standard96 | float-callback-t0-cut50-b0 | confirmations | fixed | 0.0526/0.5458 | 0.0136/0.0514 | 0.5521/1.1234 | N/A | 9.3422/9.9838 | 2034482.03 | 5.199 |
| standard96 | float-callback-t0-cut50-b1024 | initial | base | 0.0519/0.5574 | 0.0120/0.0442 | 0.5401/1.1193 | N/A | 7.6997/8.5630 | 2466441.19 | 5.164 |
| standard96 | float-callback-t0-cut50-b1024 | initial | prior | 0.0583/0.5464 | 0.0141/0.0506 | 0.5697/1.1409 | N/A | 7.9919/8.5869 | 2363435.95 | 5.180 |
| standard96 | float-callback-t0-cut50-b1024 | initial | public | 0.0601/0.5561 | 0.0140/0.0491 | 0.5675/1.1350 | N/A | 8.1516/8.7750 | 2376474.45 | 5.186 |
| standard96 | float-callback-t0-cut50-b1024 | initial | fixed | 0.0549/0.5426 | 0.0133/0.0494 | 0.5490/1.1238 | N/A | 7.7222/8.3791 | 2448624.51 | 5.199 |
| standard96 | float-callback-t0-cut100-b0 | initial | base | 0.0492/0.5717 | 0.0126/0.0443 | 3.6128/4.3107 | N/A | 7.2040/7.9788 | 53378.48 | 4.953 |
| standard96 | float-callback-t0-cut100-b0 | initial | prior | 0.0521/0.5549 | 0.0137/0.0531 | 3.7910/4.3818 | N/A | 7.5465/8.1681 | 50761.89 | 4.977 |
| standard96 | float-callback-t0-cut100-b0 | initial | public | 0.0521/0.5496 | 0.0138/0.0523 | 3.8723/4.4790 | N/A | 7.7051/8.3796 | 52080.88 | 4.984 |
| standard96 | float-callback-t0-cut100-b0 | initial | fixed | 0.0491/0.5676 | 0.0130/0.0523 | 3.6426/4.2406 | N/A | 7.2926/8.0614 | 53097.03 | 4.996 |
| standard96 | float-callback-t0-cut100-b1024 | initial | base | 0.0539/0.5840 | 0.0111/0.0460 | 3.6212/4.2767 | N/A | 7.1402/7.8428 | 53858.99 | 4.953 |
| standard96 | float-callback-t0-cut100-b1024 | initial | prior | 0.0495/0.5704 | 0.0113/0.0537 | 3.7824/4.3732 | N/A | 7.5351/8.1008 | 51176.16 | 4.977 |
| standard96 | float-callback-t0-cut100-b1024 | initial | public | 0.0529/0.5876 | 0.0118/0.0553 | 3.8835/4.5159 | N/A | 7.7038/8.4277 | 52253.98 | 4.982 |
| standard96 | float-callback-t0-cut100-b1024 | initial | fixed | 0.0485/0.5880 | 0.0109/0.0521 | 3.6771/4.2852 | N/A | 7.2898/8.0236 | 52924.94 | 4.992 |
| standard96 | float-callback-t0-cut100-b1024 | confirmations | base | 0.0533/0.5813 | 0.0120/0.0459 | 3.5787/4.2481 | N/A | 7.1319/7.8417 | 53755.09 | 4.953 |
| standard96 | float-callback-t0-cut100-b1024 | confirmations | prior | 0.0508/0.5795 | 0.0131/0.0538 | 3.8058/4.4417 | N/A | 7.5526/8.1865 | 50963.47 | 4.980 |
| standard96 | float-callback-t0-cut100-b1024 | confirmations | public | 0.0500/0.5777 | 0.0126/0.0535 | 3.8559/4.4773 | N/A | 7.6825/8.3742 | 52335.28 | 4.980 |
| standard96 | float-callback-t0-cut100-b1024 | confirmations | fixed | 0.0493/0.5617 | 0.0126/0.0540 | 3.6424/4.2718 | N/A | 7.2553/7.9093 | 53185.60 | 4.996 |
| standard96 | float-callback-t1-cut0-b0 | initial | base | 0.0611/0.5521 | 0.0132/0.0452 | 0.3546/0.9349 | N/A | 11.0697/11.5860 | 3450305.49 | 5.602 |
| standard96 | float-callback-t1-cut0-b0 | initial | prior | 0.0611/0.5512 | 0.0136/0.0521 | 0.3594/0.9349 | N/A | 11.3520/11.5928 | 3368891.82 | 5.617 |
| standard96 | float-callback-t1-cut0-b0 | initial | public | 0.0614/0.5508 | 0.0132/0.0486 | 0.3652/0.9400 | N/A | 11.2011/11.8719 | 3402086.16 | 5.637 |
| standard96 | float-callback-t1-cut0-b0 | initial | fixed | 0.0599/0.5570 | 0.0127/0.0509 | 0.3493/0.9455 | N/A | 11.1542/11.5166 | 3418329.07 | 5.584 |
| standard96 | float-callback-t1-cut0-b1024 | initial | base | 0.0525/0.5494 | 0.0123/0.0465 | 0.3354/0.9248 | N/A | 7.9571/8.6656 | 4679957.31 | 5.250 |
| standard96 | float-callback-t1-cut0-b1024 | initial | prior | 0.0541/0.5406 | 0.0113/0.0532 | 0.3488/0.9331 | N/A | 8.1834/8.8088 | 4542501.38 | 5.410 |
| standard96 | float-callback-t1-cut0-b1024 | initial | public | 0.0518/0.5471 | 0.0127/0.0522 | 0.3477/0.9453 | N/A | 8.3879/9.1080 | 4525933.51 | 5.406 |
| standard96 | float-callback-t1-cut0-b1024 | initial | fixed | 0.0560/0.5481 | 0.0132/0.0518 | 0.3458/0.9352 | N/A | 8.1787/8.8808 | 4595516.44 | 5.418 |
| standard96 | float-callback-t1-cut0-b1024 | confirmations | base | 0.0537/0.5556 | 0.0138/0.0460 | 0.3395/0.9414 | N/A | 8.0680/8.7681 | 4651236.39 | 5.250 |
| standard96 | float-callback-t1-cut0-b1024 | confirmations | prior | 0.0580/0.5529 | 0.0142/0.0534 | 0.3565/0.9424 | N/A | 8.2060/8.8401 | 4538756.34 | 5.410 |
| standard96 | float-callback-t1-cut0-b1024 | confirmations | public | 0.0535/0.5571 | 0.0141/0.0512 | 0.3561/0.9483 | N/A | 8.4288/9.1291 | 4548354.03 | 5.410 |
| standard96 | float-callback-t1-cut0-b1024 | confirmations | fixed | 0.0564/0.5695 | 0.0138/0.0510 | 0.3477/0.9595 | N/A | 8.1546/8.8295 | 4582926.75 | 5.418 |
| standard96 | float-callback-t1-cut50-b0 | initial | base | 0.0520/0.5398 | 0.0132/0.0461 | 0.5268/1.1018 | N/A | 8.9101/9.5617 | 2131961.82 | 5.105 |
| standard96 | float-callback-t1-cut50-b0 | initial | prior | 0.0545/0.5434 | 0.0140/0.0489 | 0.5429/1.1041 | N/A | 9.2078/9.7236 | 2062726.78 | 5.188 |
| standard96 | float-callback-t1-cut50-b0 | initial | public | 0.0606/0.5379 | 0.0139/0.0482 | 0.5434/1.1095 | N/A | 9.3376/10.1214 | 2069045.35 | 5.191 |
| standard96 | float-callback-t1-cut50-b0 | initial | fixed | 0.0539/0.5301 | 0.0132/0.0487 | 0.5353/1.0879 | N/A | 9.1127/9.7154 | 2097921.35 | 5.199 |
| standard96 | float-callback-t1-cut50-b0 | confirmations | base | 0.0501/0.5660 | 0.0120/0.0452 | 0.5284/1.1249 | N/A | 8.9249/9.5384 | 2119285.56 | 5.109 |
| standard96 | float-callback-t1-cut50-b0 | confirmations | prior | 0.0534/0.5741 | 0.0133/0.0501 | 0.5405/1.1242 | N/A | 9.2025/9.7412 | 2061537.37 | 5.188 |
| standard96 | float-callback-t1-cut50-b0 | confirmations | public | 0.0570/0.5439 | 0.0130/0.0490 | 0.5479/1.1186 | N/A | 9.3992/10.0346 | 2053641.33 | 5.191 |
| standard96 | float-callback-t1-cut50-b0 | confirmations | fixed | 0.0603/0.5606 | 0.0131/0.0498 | 0.5406/1.1287 | N/A | 9.0929/9.8108 | 2088801.50 | 5.199 |
| standard96 | float-callback-t1-cut50-b1024 | initial | base | 0.0508/0.5447 | 0.0126/0.0444 | 0.5370/1.1077 | N/A | 7.6504/8.2389 | 2485599.10 | 5.164 |
| standard96 | float-callback-t1-cut50-b1024 | initial | prior | 0.0540/0.5541 | 0.0136/0.0514 | 0.5413/1.1288 | N/A | 7.8078/8.3836 | 2406877.96 | 5.188 |
| standard96 | float-callback-t1-cut50-b1024 | initial | public | 0.0516/0.5514 | 0.0133/0.0487 | 0.5430/1.1136 | N/A | 8.0269/8.6580 | 2435534.50 | 5.188 |
| standard96 | float-callback-t1-cut50-b1024 | initial | fixed | 0.0611/0.5669 | 0.0132/0.0497 | 0.5362/1.1296 | N/A | 7.7359/8.5856 | 2457842.51 | 5.199 |
| standard96 | float-callback-t1-cut100-b0 | initial | base | 0.0592/0.5661 | 0.0146/0.0463 | 3.5753/4.2871 | N/A | 7.1501/7.9280 | 53992.76 | 4.949 |
| standard96 | float-callback-t1-cut100-b0 | initial | prior | 0.0600/0.5917 | 0.0131/0.0540 | 3.7050/4.3343 | N/A | 7.3779/8.0347 | 52279.59 | 4.980 |
| standard96 | float-callback-t1-cut100-b0 | initial | public | 0.0521/0.5644 | 0.0127/0.0541 | 3.7363/4.4035 | N/A | 7.4455/8.2110 | 53132.64 | 4.982 |
| standard96 | float-callback-t1-cut100-b0 | initial | fixed | 0.0623/0.5669 | 0.0127/0.0521 | 3.5966/4.1893 | N/A | 7.1744/7.9122 | 53369.64 | 4.977 |
| standard96 | float-callback-t1-cut100-b0 | confirmations | base | 0.0513/0.5692 | 0.0147/0.0444 | 3.5741/4.2410 | N/A | 7.1082/7.8746 | 54325.61 | 4.953 |
| standard96 | float-callback-t1-cut100-b0 | confirmations | prior | 0.0502/0.5558 | 0.0138/0.0539 | 3.6659/4.2909 | N/A | 7.3130/7.9963 | 52412.45 | 4.984 |
| standard96 | float-callback-t1-cut100-b0 | confirmations | public | 0.0600/0.5711 | 0.0141/0.0540 | 3.7508/4.4029 | N/A | 7.4602/8.1456 | 53177.19 | 4.980 |
| standard96 | float-callback-t1-cut100-b0 | confirmations | fixed | 0.0508/0.5709 | 0.0132/0.0528 | 3.6220/4.2426 | N/A | 7.2036/7.9381 | 53497.84 | 4.984 |
| standard96 | float-callback-t1-cut100-b1024 | initial | base | 0.0496/0.5370 | 0.0122/0.0441 | 3.6253/4.1833 | N/A | 7.1873/7.7213 | 54370.58 | 4.947 |
| standard96 | float-callback-t1-cut100-b1024 | initial | prior | 0.0576/0.5587 | 0.0133/0.0549 | 3.6684/4.2492 | N/A | 7.2980/7.9523 | 52581.55 | 4.977 |
| standard96 | float-callback-t1-cut100-b1024 | initial | public | 0.0521/0.5479 | 0.0132/0.0521 | 3.7426/4.3616 | N/A | 7.5003/8.1720 | 53757.98 | 4.975 |
| standard96 | float-callback-t1-cut100-b1024 | initial | fixed | 0.0495/0.5493 | 0.0126/0.0514 | 3.5890/4.2443 | N/A | 7.1325/7.8720 | 54204.44 | 4.986 |
| longname14 | long-n0-b0-parallel0 | initial | public | 0.0701/0.5966 | 0.0175/0.0608 | 2.1500/2.9597 | 0.0033/0.0071 | 31.0395/36.6386 | 417042.28 | 5.418 |
| longname14 | long-n0-b0-parallel0 | initial | fixed | 0.0696/0.5664 | 0.0175/0.0605 | 2.1492/2.9030 | 0.0032/0.0065 | 30.7950/35.2735 | 417661.07 | 5.420 |
| longname14 | long-n0-b0-parallel1 | initial | public | 0.0693/0.5904 | 0.0180/0.0608 | 2.1423/2.8847 | 0.0027/0.0064 | 30.7871/35.2605 | 418181.46 | 5.402 |
| longname14 | long-n0-b0-parallel1 | initial | fixed | 0.0651/0.5610 | 0.0183/0.0607 | 2.1736/2.9252 | 0.0030/0.0065 | 31.2342/35.6551 | 414423.01 | 5.404 |
| longname14 | long-n0-b0-parallel1 | confirmations | public | 0.0691/0.6000 | 0.0184/0.0614 | 2.1515/2.9374 | 0.0031/0.0066 | 31.0319/35.8053 | 416713.36 | 5.402 |
| longname14 | long-n0-b0-parallel1 | confirmations | fixed | 0.0688/0.5729 | 0.0188/0.0596 | 2.1757/2.9252 | 0.0034/0.0067 | 31.0382/36.1791 | 414253.99 | 5.410 |
| longname14 | long-n0-b1-parallel0 | initial | public | 0.0694/0.5553 | 0.0175/0.0581 | 0.1647/0.7396 | 0.0028/0.0110 | 29.9691/31.7567 | 458623.01 | 5.438 |
| longname14 | long-n0-b1-parallel0 | initial | fixed | 0.0653/0.5723 | 0.0172/0.0595 | 0.1651/0.7555 | 0.0029/0.0120 | 30.1510/31.1727 | 454882.55 | 5.434 |
| longname14 | long-n0-b1-parallel1 | initial | public | 0.0715/0.5478 | 0.0180/0.0599 | 0.1671/0.7245 | 0.0029/0.0122 | 29.3887/31.1107 | 463950.34 | 5.430 |
| longname14 | long-n0-b1-parallel1 | initial | fixed | 0.0717/0.5876 | 0.0195/0.0596 | 0.1726/0.7729 | 0.0032/0.0121 | 30.1189/33.0189 | 458288.12 | 5.430 |
| longname14 | long-n0-b1-parallel1 | confirmations | public | 0.0650/0.5784 | 0.0176/0.0594 | 0.1640/0.7580 | 0.0026/0.0117 | 29.8527/32.2242 | 458559.13 | 5.434 |
| longname14 | long-n0-b1-parallel1 | confirmations | fixed | 0.0680/0.5681 | 0.0179/0.0605 | 0.1632/0.7518 | 0.0026/0.0115 | 30.0286/31.4516 | 458518.77 | 5.434 |
| longname14 | long-n0-b1024-parallel0 | initial | public | 0.0675/0.5693 | 0.0176/0.0583 | 2.1364/3.2660 | 0.0027/0.0067 | 26.5389/29.7142 | 491713.86 | 5.477 |
| longname14 | long-n0-b1024-parallel0 | initial | fixed | 0.0674/0.5706 | 0.0183/0.0601 | 2.1576/2.9079 | 0.0028/0.0132 | 28.0703/29.3587 | 483134.44 | 5.467 |
| longname14 | long-n0-b1024-parallel0 | confirmations | public | 0.0687/0.5748 | 0.0177/0.0587 | 2.1590/3.2929 | 0.0028/0.0072 | 27.9957/29.7192 | 485372.64 | 5.473 |
| longname14 | long-n0-b1024-parallel0 | confirmations | fixed | 0.0706/0.5725 | 0.0180/0.0601 | 2.1595/2.9575 | 0.0028/0.0119 | 28.2926/33.1347 | 482529.76 | 5.469 |
| longname14 | long-n0-b1024-parallel1 | initial | public | 0.0675/0.5613 | 0.0176/0.0588 | 2.1747/3.2555 | 0.0027/0.0065 | 28.2660/31.4551 | 482481.91 | 5.471 |
| longname14 | long-n0-b1024-parallel1 | initial | fixed | 0.0638/0.5749 | 0.0174/0.0594 | 2.1527/2.9105 | 0.0026/0.0120 | 28.2206/29.6563 | 482908.32 | 5.467 |
| longname14 | long-n1-b0-parallel0 | initial | public | 0.0727/0.5767 | 0.0181/0.0569 | 1.1764/1.9150 | 0.0036/0.0073 | 41.5012/46.7886 | 624578.16 | 5.539 |
| longname14 | long-n1-b0-parallel0 | initial | fixed | 0.0731/0.5675 | 0.0181/0.0596 | 1.1988/1.9257 | 0.0034/0.0074 | 41.6237/47.5751 | 623619.72 | 5.539 |
| longname14 | long-n1-b0-parallel1 | initial | public | 0.0750/0.5573 | 0.0186/0.0576 | 1.1697/1.8905 | 0.0038/0.0076 | 41.5603/46.4331 | 622599.05 | 5.535 |
| longname14 | long-n1-b0-parallel1 | initial | fixed | 0.0723/0.5692 | 0.0180/0.0620 | 1.1759/1.9059 | 0.0032/0.0077 | 41.5643/47.1555 | 621459.82 | 5.539 |
| longname14 | long-n1-b1-parallel0 | initial | public | 0.0767/0.5868 | 0.0189/0.0561 | 0.1797/0.7643 | 0.0034/0.0098 | 29.1971/32.8269 | 884368.63 | 5.549 |
| longname14 | long-n1-b1-parallel0 | initial | fixed | 0.0726/0.5619 | 0.0191/0.0582 | 0.1679/0.7417 | 0.0030/0.0094 | 30.9165/35.9855 | 867574.94 | 5.543 |
| longname14 | long-n1-b1-parallel1 | initial | public | 0.0767/0.5635 | 0.0191/0.0583 | 0.1864/0.7422 | 0.0029/0.0101 | 31.4955/36.0572 | 874173.82 | 5.547 |
| longname14 | long-n1-b1-parallel1 | initial | fixed | 0.0752/0.5805 | 0.0197/0.0587 | 0.1719/0.7641 | 0.0033/0.0102 | 31.8826/36.3757 | 858164.65 | 5.545 |
| longname14 | long-n1-b1024-parallel0 | initial | public | 0.0651/0.5652 | 0.0177/0.0572 | 1.1788/2.1026 | 0.0026/0.0063 | 28.7347/33.2718 | 949615.30 | 5.578 |
| longname14 | long-n1-b1024-parallel0 | initial | fixed | 0.0639/0.5647 | 0.0174/0.0557 | 1.1713/1.9256 | 0.0026/0.0100 | 28.2678/32.3846 | 950271.65 | 5.578 |
| longname14 | long-n1-b1024-parallel1 | initial | public | 0.0717/0.5837 | 0.0192/0.0594 | 1.1821/2.1484 | 0.0029/0.0077 | 28.9443/32.2770 | 960192.06 | 5.578 |
| longname14 | long-n1-b1024-parallel1 | initial | fixed | 0.0715/0.5751 | 0.0202/0.0584 | 1.1902/1.9213 | 0.0033/0.0105 | 28.5832/30.2074 | 948195.83 | 5.578 |
| longname14 | long-n0-b0-parallel0-early | initial | public | 0.0491/0.5214 | 0.0132/0.0536 | 2.1063/2.8195 | 0.0321/0.0481 | 2.1535/2.8920 | 425.34 | 5.090 |
| longname14 | long-n0-b0-parallel0-early | initial | fixed | 0.0466/0.5260 | 0.0129/0.0559 | 2.1049/2.8760 | 0.0316/0.0500 | 2.1433/2.9438 | 420.57 | 5.094 |
| longname14 | long-n0-b0-parallel0-early | confirmations | public | 0.0488/0.5445 | 0.0129/0.0556 | 2.1136/2.8518 | 0.0327/0.0480 | 2.1562/2.9176 | 421.56 | 5.092 |
| longname14 | long-n0-b0-parallel0-early | confirmations | fixed | 0.0486/0.5329 | 0.0129/0.0555 | 2.1089/2.8704 | 0.0319/0.0476 | 2.1521/2.9408 | 420.38 | 5.090 |
| longname14 | long-n1-b0-parallel0-early | initial | public | 0.0485/0.5014 | 0.0132/0.0506 | 1.1573/1.8145 | 0.0297/0.0400 | 1.2007/1.8720 | 718.84 | 5.150 |
| longname14 | long-n1-b0-parallel0-early | initial | fixed | 0.0450/0.5087 | 0.0124/0.0511 | 1.1715/1.8343 | 0.0299/0.0398 | 1.2135/1.8925 | 708.11 | 5.199 |
| longname14 | long-n1-b0-parallel0-early | confirmations | public | 0.0486/0.5016 | 0.0136/0.0508 | 1.1628/1.7990 | 0.0307/0.0399 | 1.2062/1.8584 | 718.91 | 5.148 |
| longname14 | long-n1-b0-parallel0-early | confirmations | fixed | 0.0490/0.5020 | 0.0139/0.0507 | 1.1756/1.8401 | 0.0301/0.0414 | 1.2185/1.8986 | 708.06 | 5.150 |
