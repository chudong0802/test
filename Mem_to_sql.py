import pandas as pd
import os 
import datetime,time
import pymysql


def deal_file(path):
    dir_name = os.listdir(path)
    print(dir_name)
    for n in range(len(dir_name)):
        sub_path=os.path.join(path,dir_name[n])
        print(sub_path)
        if os.path.isdir(sub_path):
            sub_fname = os.listdir(sub_path)
            print(sub_fname)
            if 'analysis' in sub_fname:
                try:
                    conn = pymysql.connect(host='10.16.31.77',user='root',password='AutoTest',port=3306,database='chart_demo')
                    cursor = conn.cursor()
                    if 'dumpSFalwarys.csv' in os.listdir(sub_path+'/analysis'):
                        print('exist')
                        fdata = pd.read_csv(sub_path+'/analysis'+'/dumpSFalwarys.csv',encoding='utf-8')
                        df_data = pd.DataFrame(fdata)
                        print(df_data)
                        for i in range(len(df_data['time'])):
                            timestring = str(df_data['time'][i])
                            print(timestring)
                            try:
                                create_time = datetime.datetime.fromtimestamp(
                                    time.mktime(time.strptime(timestring,"%Y-%m-%d %H:%M:%S")))
                            except Exception:
                                continue
                            total_allocated = df_data['total_allocated(KB)'][i]
                            display_0_layer = df_data['display_0_layer'][i]
                            display_1_layer = df_data['display_1_layer'][i]
                            buffers = df_data['buffers'][i]
                            print(buffers)
                            sql1 = "insert into dumpSFalwarys (time,total_allocated,display_0_layer,display_1_layer,buffers)"\
                                    "values('%s','%f','%d','%d','%d')"%(create_time,total_allocated,display_0_layer,display_1_layer,buffers)
                            print(sql1)
                            try:
                                cursor.execute(sql1)
                                conn.commit()
                                print('........')
                            except:
                                conn.rollback()
                                print('=======')
                    
                    if 'ionmemalways.csv' in os.listdir(sub_path+'/analysis'):
                        print('exist')
                        mdata = pd.read_csv(sub_path+'/analysis'+'/ionmemalways.csv',encoding='utf-8')
                        df_mdata = pd.DataFrame(mdata)
                        for j in range(len(df_mdata['time'])):
                            mtimestring = str(df_mdata['time'][j])
                            try:
                                create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(mtimestring,"%Y-%m-%d %H:%M:%S")))
                            except Exception:
                                continue
                            surfaceflinger_size = df_mdata['surfaceflinger_size(Byte)'][j]
                            total_size = df_mdata['total_size(Byte)'][j]
                            sql2 = "insert into ionmemalways (time,surfaceflinger_size,total_size)"\
                                    "values('%s','%d','%d')"%(create_time,surfaceflinger_size,total_size)
                            print(sql2)
                            try:
                                cursor.execute(sql2)
                                conn.commit()
                                print('........')
                            except:
                                conn.rollback()
                                print('=======')
                    
                    if 'meminfo.csv' in os.listdir(sub_path+'/analysis'):
                        kdata = pd.read_csv(sub_path+'/analysis'+'/meminfo.csv',encoding='utf-8')
                        df_kdata = pd.DataFrame(kdata)
                        for k in range(len(df_kdata)):
                            ktimestring = str(df_kdata['time'][k])
                            try:
                                create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ktimestring,"%Y-%m-%d %H:%M:%S")))
                            except Exception:
                                continue
                            contig_len = df_kdata['contig_len(MB)'][k]
                            non_contig_len = df_kdata['non_contig_len(MB)'][k]
                            sql3 = "insert into meminfo(time,contig_len,non_contig_len)"\
                                    "values('%s','%.2f','%.2f')"%(create_time,contig_len,non_contig_len)
                            print(sql3)
                            try:
                                cursor.execute(sql3)
                                conn.commit()
                                print('........')
                            except:
                                conn.rollback()
                                print('=======')
                    
                    cursor.close()
                    conn.close()
                except:
                    continue


if __name__ == "__main__":
    deal_file('./')
    