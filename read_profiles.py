# read atmospheric profiles according to their formats
import numpy as np

# SeeBor
pressure_seebor = [0.005,0.016,0.038,0.077,0.137,0.224,0.345,0.506,0.714,0.975,1.297,1.687,2.153,2.701,3.340,4.077,4.920,
                   5.878,6.957,8.165,9.512,11.004,12.649,14.456,16.432,18.585,20.922,23.453,26.183,29.121,32.274,35.651,39.257,
                   43.100,47.188,51.528,56.126,60.989,66.125,71.540,77.240,83.231,89.520,96.114,103.017,110.237,117.777,125.646,133.846,
                   142.385,151.266,160.496,170.078,180.018,190.320,200.989,212.028,223.441,235.234,247.408,259.969,272.919,286.262,300.000,314.137,
                   328.675,343.618,358.966,374.724,390.893,407.474,424.470,441.882,459.712,477.961,496.630,515.720,535.232,555.167,575.525,596.306,
                   617.511,639.140,661.192,683.667,706.565,729.886,753.628,777.790,802.371,827.371,852.788,878.620,904.866,931.524,958.591,986.067,
                   1013.948,1042.232,1070.917,1100.000]
def Read_Seebor(file_path):
    '''
    Record number:15,704    Record length: 338  Datatype: real*4
    1:101 temperature profile [K]
    102:202 mixing ratio profile [kg/kg]
    203:303 ozone profile [ppmv]
    309 tpw [cm]
    312 fraction land
    pressure in hPa (1 hPa = 1 mb)
    '''
    # convert binary data into float32 (real4)
    data = np.fromfile(file_path, dtype=np.float32)
    tem, h2o, o3, tpw, fraction_land, h = [], [], [], [], [], []
    for i in range(15704):
        data_i = data[i*338:(i+1)*338].copy()
        tem.append(data_i[0:101])
        h2o.append(data_i[101:202])
        o3.append(data_i[202:303])
        tpw.append(data_i[308])
        fraction_land.append(data_i[311])
        h.append(data_i[310]/1e3) # m->km
    return np.array(tem), np.array(h2o), np.array(o3), np.array(tpw), np.array(fraction_land), np.array(h)


# TIGR
def Read_TIGR(TIGR_path, rule, threshold):
    '''
    读取TIGR大气廓线，将气象元素存储在数组中
    然后根据输入的准则与阈值筛选出合格的大气廓线
    :param TIGR_path: TIGR .dsf数据集文件路径
    :return:array of tem h2o o3

    * 共2311条数据 每条数据的格式如下：
    * iatm,ilat,ilon,idate   format(4I12)
    * 气温T                   format(6E12.5)*6 format(4E12.5)
    * 地表温度和气压            format(2E12.5)
    * RO_H2O                 format(6E12.5)*6 format(4E12.5)
    * RO_O3                  format(6E12.5)*6 format(4E12.5)
    '''

    # TIGR 大气廓线40层每层的气压(从大气层顶到地表)
    pressure = [0.5E-01, 0.8999997E-01, 0.17E+00, 0.3E+00, 0.55E+00,
                0.1E+01, 0.15E+01, 0.223E+01, 0.333E+01, 0.498E+01,
                0.743E+01, 0.1111E+02, 0.1660001E+02, 0.2478999E+02, 0.3703999E+02,
                0.4573E+02, 0.5646001E+02, 0.6971001E+02, 0.8607001E+02, 0.10627E+03,
                0.1312E+03, 0.16199E+03, 0.2E+03, 0.22265E+03, 0.24787E+03,
                0.27595E+03, 0.3072E+03, 0.34199E+03, 0.38073E+03, 0.4238501E+03,
                0.4718601E+03, 0.525E+03, 0.5848E+03, 0.65104E+03, 0.72478E+03,
                0.8E+03, 0.8486899E+03, 0.9003301E+03, 0.9551201E+03, 0.1013E+04]

    tem_surface = []
    tem = [[] for i in range(3000)]
    h2o = [[] for i in range(3000)]
    o3 = [[] for i in range(3000)]

    line_read = 0  # 指示读取到的行号
    line_unit = 23  # 一条廓线占据23行
    order = -1  # 大气廓线序号

    with open(TIGR_path, encoding='utf-8') as obj:
        for string in obj:
            line_read = line_read + 1
            remainder = line_read % line_unit
            line = string.strip("\n")

            if remainder == 1:
                order = order + 1

            if 2 <= remainder <= 8:
                tem_array = line.split()  #.split()忽略所有空格
                for tem_split in tem_array:
                    tem[order].append(float(tem_split))

            if remainder == 9:
                tem_surface.append(float(line.split()[0]))

            if 10 <= remainder <= 16:
                h2o_array = line.split()
                for h2o_split in h2o_array:
                    h2o[order].append(float(h2o_split) * 1000)  # 混合比单位 g/g->g/kg

            if 17 <= remainder <= 22 or remainder == 0:
                o3_array = line.split()
                for o3_split in o3_array:
                    o3[order].append(float(o3_split) * 1000)

    if rule == "RH":  # 相对湿度
        qualified_order = []
        p = np.array(pressure) * 100  # mbar->pa
        for i in range(len(tem_surface)):
            Tc_everyProfile = np.array(tem[i]) - 273.15  # 转换为摄氏温度
            w = np.array(h2o[i])
            es = 611 * np.exp(17.27 * Tc_everyProfile / (237.3 + Tc_everyProfile))  # 饱和水气压 单位：pa
            ws = 622 * es / (p - es)  # 饱和混合比g/kg
            RH = 100 * w / ws

            compare_results = RH > threshold
            if (True in compare_results) == False:
                qualified_order.append(i)
                
    if rule == "all":
        qualified_order = [i for i in range(order + 1)]

    return tem_surface, tem, h2o, o3, qualified_order, pressure