# read the output files (.tp7 and .flx) from MODTRAN
import numpy as np

def Read_tp7(tp7_path, ref=0.05, idx=[1,2,4]):
    with open(tp7_path, "r") as f:
        tp7 = f.read()
    f.close()
    num_profile = tp7.count('GRND_RFLT')
    
    wn = []
    tran = [[] for _ in range(num_profile)]
    L_up = [[] for _ in range(num_profile)]
    L_dn = [[] for _ in range(num_profile)]
    start = 0
    num = -1

    with open(tp7_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            if line == " -9999.":
                start = 0

            if start == 1:
                parameter_array = line.split()
                # convert W/cm^2/sr/cm^-1 to W/m^2/sr/cm^-1
                tran_wn_i, L_up_wn_i, L_grd_ref_wn_i = float(parameter_array[idx[0]]), float(parameter_array[idx[1]]) * 1E4, float(parameter_array[idx[2]]) * 1E4
                tran[num].append(tran_wn_i)
                L_up[num].append(L_up_wn_i)
                if tran_wn_i == 0:
                    L_dn[num].append(-999)
                else:
                    L_dn_wn_i = L_grd_ref_wn_i/ref/tran_wn_i
                    L_dn[num].append(L_dn_wn_i)
                if num == 0:
                    wn.append(float(parameter_array[0]))

            if "GRND_RFLT" in line:
                start = 1
                num = num + 1
    f.close()

    wn, tran, L_up, L_dn = np.array(wn), np.array(tran), np.array(L_up), np.array(L_dn)
    L_dn[L_dn == -999] = np.nan
    return wn, tran, L_up, L_dn

def Read_flx(flx_path, num_profile):
    SDLR = [[] for _ in range(num_profile)]
    start = 0
    num = -1

    with open(flx_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            if "DIFFUSE" in line:
                start = 1
                num = num + 1
                continue
            
            if "=======" in line:
                start = 0

            if (start == 1) and ('-------' not in line):
                parameter_array = line.split()
                # convert W/cm^2/cm^-1 to W/m^2/cm^-1
                SDLR[num].append(float(parameter_array[2]) * 1E4)
    f.close()

    return np.array(SDLR)