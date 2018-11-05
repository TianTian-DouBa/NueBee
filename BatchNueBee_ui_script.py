from BatchNueBee_ui import Ui_MW_BatchNueBee
from PyQt5 import QtWidgets
import sys
from datetime import datetime, timedelta
from subprocess import Popen #debug
from XF_common.XF_UTC_LOCAL import *
from XF_common.XF_SQL import DV_SOE
from XF_common.XF_SERIALIZING import *
from XF_common.XF_LOG_MANAGE import add_log, logable, log_print
from XF_common.XF_PATH import list_file_names
from XF_common.XF_XML import create_raw_1pt_xml,create_raw_mpt_xml, generate_xml,valid_xml,read_1pt,read_mpt,XML_CONSTANT
from XF_common.XF_DV_HIST import execute_xml, Value_Log, valid_batch_id #debug

BATCH_STATUS = ('Undefined','Running','Completed','Void')
DEF_PACKED_PATH = r".\packed" + "\\"
VESSEL_LAST_SCAN_SURFIX = "_last_scan.dtp"
VESSEL_BATCH_ITEMS_SURFIX = "_batches.dtp"
INIT_TIME_STRING = "2010-01-01 00:00:00"  #默认初始时间字符串
VESSEL_NAME_LIST = ['V1','V2'] #to be modified according to Unit_info
TIME_STAMP_ORDER = ('match','batch_item_early','last_log_early','no_log')
RUNNING_EXPIRE_DAYS = 50 #超过此限值的Running Batch判断为‘underfined’

vessels = {} #Dict，存储Vessel类的实例
vessels_batch_items = {} #Dict，存储类的实例
ej_db_profile = None #<Soe_Db_Profile> for EJournal
soe_db_profiles = [] #<list>, 存储Soe_Db_Profile实例
soe_db_files = [] #<list>, .mdf的主文件名列表

class MainWindow(Ui_MW_BatchNueBee, QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        #初始化参数
        self.DEF_START_TIME = datetime.strptime("2010-01-01 00:30:00", \
                                                "%Y-%m-%d %H:%M:%S") #默认开始扫描时间
        #额外界面设置

        #在此，可添加自定义的信号绑定
        self.pushButton.clicked.connect(lambda: self.batch_split(vessel_no = 'V1')) #test
        self.pushButton_test_temp1.clicked.connect(self.tst_temp1) #test
        self.pushButton_test_temp2.clicked.connect(self.tst_temp2) #test
        self.pushButton_test_temp3.clicked.connect(self.tst_temp3) #test
        self.pushButton_test_temp4.clicked.connect(self.tst_temp4) #test

    def model_init(self):
        """从文件读入批次列表和前次扫描信息，初始化vessels"""
        global vessels
        for vessel_no in VESSEL_NAME_LIST:
            v = Vessel(vessel_no)
            vessels[vessel_no] = v

    def soe_dbs_profile(self):
        """在SOE Server上，在线的SOE存储文件的启止时间档案
        - [global] soe_db_profiles: 插入有效的soe_db对应的<Soe_Db_Profile>
        - [global] ej_db_profile: 根据EJournal db改写"""
        global soe_db_files, soe_db_profiles, ej_db_profile
        soe_db_profiles = []
        dv_soe = DV_SOE()

        def take_start(obj):
            """返回Soe_Db_Profile.db_start_time,用于自定义方法排序"""
            return obj.db_start_time

        if dv_soe.conn == None: #判断pymssql.connect是否成功
            add_log(10,'fn:soe_dbs_profile();sql connection fail, aborted')
            return
        db_names =  dv_soe.db_names()
        try:
            db_names.index('EJournal')
        except ValueError:
            print_log(10, 'fn:soe_dbs_profile(), "EJournal" is not in db_names')
            return

        path = r'D:\DeltaV\DVData\CHRONICLE'
        extension = '.mdf'
        _br = list_file_names(path,extension)
        if _br[0] == 'Normal':
            soe_db_files = []
            for i in _br[1]:
                soe_db_files.append(i[len(path)+1:-len(extension)])

        add_log(30, 'fn:soe_dbs_profile() Start ===================')
        log_args = [_br[0]]
        add_log(30, 'fn:soe_dbs_profile(), files browse status: {0[0]}',log_args)
        if logable(30):
            for i in soe_db_files:
                log_print(i)
        add_log(30, 'fn:soe_dbs_profile() End ===================')

        try:
            soe_db_files.index('EJournal')
        except ValueError:
            add_log(10, 'fn:soe_dbs_profile(), "EJournal" is not in soe_db_files')
            return

        for i in db_names:
            if i == 'EJOverflow':
                continue
            else:
                try:
                    soe_db_files.index(i) #如果数据库名与目录中的SOE数据库文件名吻合
                    if i == 'EJournal':
                        ej_db_profile = Soe_Db_Profile(i)
                    else:
                        soe_db_profiles.append(Soe_Db_Profile(i))
                except ValueError:
                    log_args = [i]
                    add_log(40, 'fn:soe_dbs_profile(), {0[0]} filtered out', log_args)
        soe_db_profiles.sort(key=take_start,reverse=False)

    def print_soe_db_profiles(self):
        """显示soe_db_profiles的内容"""
        global soe_db_profiles, ej_db_profile
        print("[fn] print_soe_db_profiles() start ================")
        print(".db_name = {}".format(ej_db_profile.db_name))
        print(".db_start_time = {}".format(ej_db_profile.db_start_time))
        print(".db_end_time = {}".format(ej_db_profile.db_end_time))
        print("----------------------------------------")
        for i in soe_db_profiles:
            print(".db_name = {}".format(i.db_name))
            print(".db_start_time = {}".format(i.db_start_time))
            print(".db_end_time = {}".format(i.db_end_time))
            print("----------------------------------------")
        print("[fn] print_soe_db_profiles() end ================")

    def tst_temp1(self):
        """temp to delete"""
        print("===============tst_temp1 strat==============")
        main.model_init()
        for i in vessels.values():
            print('--------------------------------------')
            print(i.vessel_no)
            print(i.last_scan.vessel_no)
            print(i.last_scan.last_batch_status)
            print(i.last_scan.last_log_time)
            print(type(i.last_scan.last_log_time))
            print(i.last_scan.last_log_frac_sec)
            print(i.batch_items)
        print("===============tst_temp1 end==============")

    def tst_temp2(self):
        """create XML and execute"""
        print("===============tst_temp2 strat==============")
        #xml_path = r'.\packed\temp\raw_1pt.xml'
        #execute_xml(xml_path)
        #Popen(["notepad", r".\packed\temp\raw_1pt.csv"])
        dt = string_to_dt("2018-10-22 13:34:23")
        item_id = r"V1-COMMON/BATCH_ID.CV"
        element_tree = create_raw_1pt_xml(dt,item_id)
        xml_path = r'.\packed\temp\_raw_1pt.tmp'
        generate_xml(element_tree,xml_path)
        #with open(r'.\packed\temp\_raw_1pt.tmp','r') as xml:
            #valid_xml(r'.\packed\temp\DvOpcHda.xsd',xml)
        element_tree = None
        execute_xml(xml_path)
        result_path = r".\packed\temp\raw_1pt_opt.xml"
        read_1pt(result_path)

        element_tree = create_raw_1pt_xml(dt,item_id)
        xml_path = r'.\packed\temp\_raw_1pt.tmp'
        generate_xml(element_tree,xml_path)
        with open(r'.\packed\temp\_raw_1pt.tmp','r') as xml:
            valid_xml(r'.\packed\temp\DvOpcHda.xsd',xml)
        element_tree = None
        execute_xml(xml_path)
        result_path = r".\packed\temp\raw_1pt_opt.xml"
        read_raw_1pt(result_path)

        start_time = string_to_dt("2018-10-08 13:34:23")
        end_time = string_to_dt("2018-10-10 13:34:23")
        element_tree = create_raw_mpt_xml(start_time,end_time,item_id)
        xml_path = r'.\packed\temp\_raw_mpt.tmp'
        generate_xml(element_tree,xml_path)
        with open(r'.\packed\temp\_raw_mpt.tmp','r') as xml:
            valid_xml(r'.\packed\temp\DvOpcHda.xsd',xml)
        element_tree = None
        execute_xml(xml_path)
        result_path = r".\packed\temp\raw_mpt_opt.xml"
        read_mpt(result_path)
        #Popen(["notepad", r".\packed\temp\raw_mpt_opt.xml"])
        print("===============tst_temp2 end==============")

    def tst_temp3(self):
        """temp to delete"""
        print("===============tst_temp3 strat==============")
        start_s = datetime.now()
        main.model_init()
        main.soe_dbs_profile()
        main.print_soe_db_profiles() #opitional
        v=vessels["V1"]
        start_time = v.return_scan_time()[1]
        if not isinstance(start_time,datetime):
            print("start_time was: {}".format(start_time))
            start_time = datetime.strptime ("2014-08-18 02:47:25.8160", "%Y-%m-%d %H:%M:%S.%f")
        print("multi_dbs_enquiry().start_time:{}".format(start_time))
        rslt_batch_start = v.multi_dbs_enquiry(start_time)
        #v.print_vessel_last_scan()
        #v.print_batch_items()
        print("********")
        v.fill_batch_items(rslt_batch_start)
        v.print_batch_items()

        start_e = datetime.now()
        print(start_e - start_s)
        print("===============tst_temp3 end==============")

    def tst_temp4(self):
        """main test, [fn]complete_batch_item"""
        print("===============tst_temp4 strat==============")
        start_s = datetime.now()
        main.model_init()
        main.soe_dbs_profile()
        main.print_soe_db_profiles() #opitional
        v=vessels["V1"]
        start_time = v.return_scan_time()[1]
        if not isinstance(start_time,datetime):
            print("start_time was: {}".format(start_time))
            start_time = datetime.strptime ("2014-08-18 02:47:25.8160", "%Y-%m-%d %H:%M:%S.%f")
        print("multi_dbs_enquiry().start_time:{}".format(start_time))
        rslt_batch_start = v.multi_dbs_enquiry(start_time)
        #v.print_vessel_last_scan()
        #v.print_batch_items()
        print("********")
        v.fill_batch_items(rslt_batch_start)
        #v.print_batch_items()
        #for item in v.batch_items:
        #    item.complete_batch_item()
        v.print_batch_items()
        v.update_last_scan()
        v.print_vessel_last_scan()
        v.dump_vessel_last_scan()
        v.dump_vessel_batch_items()

        start_e = datetime.now()
        print(start_e - start_s)
        print("===============tst_temp4 end==============")

    def on_exit(self):
        """放程序退出前的必要动作"""
        pass

class Vessel():
    """Vessel维度的状态"""
    def __init__(self, vessel_number):
        self.vessel_no = vessel_number
        _load_rslt = self.load_vessel_last_scan()
        if isinstance(_load_rslt,Vessel_Last_Scan):
            self.last_scan = _load_rslt
            log_args = [vessel_number]
            add_log(30, '"{0[0]}".__init__() last_scan loaded from file', log_args)
        else:
            self.last_scan = Vessel_Last_Scan()
            self.last_scan.last_batch_status = BATCH_STATUS[0] #'Underfined'
            self.last_scan.last_log_frac_sec = 0
            self.last_scan.last_log_time = string_to_dt(INIT_TIME_STRING)
            log_args = [vessel_number]
            add_log(30, '"{0[0]}".__init__() last_scan created with default value', log_args)
        self.batch_items = self.load_vessel_batch_items()

    def multi_dbs_enquiry(self, start_time, server = 'localhost'):
        """跨多个数据库文件查询Batch_Start
        return: <list> <- <Batch_Start_Log>
        - start_time: <datetime> in UTC e.g. '2018-08-18 02:46:51.32130000'
        - server: <str>SOE host station"""
        global ej_db_profile, soe_db_profiles
        result = []
        end_time = datetime.now()
        module = self.vessel_no + '-COMMON'
        if start_time < ej_db_profile.db_start_time:
            for db in soe_db_profiles:
                if db.db_end_time < start_time:
                    continue
                else:
                    if db.db_end_time > ej_db_profile.db_start_time:
                        _db_end_time = ej_db_profile.db_start_time
                        dv_soe = DV_SOE(server,db.db_name)
                        _rslt = dv_soe.enquiry(dv_soe.sql_batch_start(module,start_time, _db_end_time))
                        if len(_rslt) > 0:
                            result.append(_rslt)
                        dv_soe.close()
                        dv_soe = None
                        break
                    else:
                        _db_end_time = ej_db_profile.db_start_time
                        dv_soe = DV_SOE(server,db.db_name)
                        _rslt = dv_soe.enquiry(dv_soe.sql_batch_start(module,start_time, _db_end_time))
                        if len(_rslt) > 0:
                            result.append(_rslt)
                        dv_soe.close()
                        dv_soe = None
                        continue
        ej_soe = DV_SOE(server)
        _rslt = ej_soe.enquiry(ej_soe.sql_batch_start(module,start_time))
        if len(_rslt) > 0:
            result.extend(_rslt)
        ej_soe.close()
        ej_soe = None
        add_log(30,'<fn>multi_dbs_enquiry().return start=============')
        if logable(30):
            for i in result:
                print(i)
        add_log(30,'<fn>multi_dbs_enquiry().return end=============')
        return result

    def fill_batch_items(self,batch_start_list):
        """fill vessel.batch_items"""
        def _new_batch_item():
            """instance new batch_item from Batch_Item. internal use only"""
            item = Batch_Item()
            item.batch_start_time = log_time
            item.batch_status = BATCH_STATUS[1] #'Running'
            item.vessel_no = self.vessel_no
            self.batch_items.append(item)

        for log in batch_start_list:
            log_time = frac_to_msec(log[1],log[2]) #convert log time to datatime is msec
            if len(self.batch_items) > 0:
                last_batch = self.batch_items[-1]
                if last_batch.batch_status == BATCH_STATUS[1]: #'Running'
                    if log[0] == '0': #parameter of batch_start_time
                        last_batch.batch_end_time = log_time
                        last_batch.batch_status = BATCH_STATUS[2] #'Completed'
                        last_batch.complete_batch_item()
                    elif log[0] == '1':
                        running_last = log_time - last_batch.batch_start_time
                        if running_last > timedelta(days=RUNNING_EXPIRE_DAYS):
                            last_batch.batch_status = BATCH_STATUS[0] #'underfined'
                            last_batch.comment = "set to 'undefined' by system"
                            _new_batch_item()
                        else:
                            log_args = [log]
                            add_log(20, '[fn]fill_batch_items(); log discarded due to status conflicted with previous one. log:"{0[0]}"', log_args)
                    else:
                        log_args = [log[0]]
                        add_log(10,'[fn]fill_batch_items() log[0]:"{0[0]}" not in "0" or "1"',log_args)
                else: # not 'Running'
                    if log[0] == '1': #parameter of batch_start_time
                        _new_batch_item()
                    elif log[0] == '0':
                        log_args = [log]
                        add_log(20, '[fn]fill_batch_items(); log discarded due to status conflicted with previous one. log:"{0[0]}"', log_args)
                    else:
                        log_args = [log[0]]
                        add_log(10,'[fn]fill_batch_items() log[0]:"{0[0]}" not in "0" or "1"',log_args)
            else:
                if log[0] == '1': #parameter of batch_start_time
                    _new_batch_item()
                elif log[0] == '0':
                    log_args = [log]
                    add_log(20, '[fn]fill_batch_items(); log discarded due to status conflicted with previous one. log:"{0[0]}"', log_args)
                else:
                    log_args = [log[0]]
                    add_log(10,'[fn]fill_batch_items() log[0]:"{0[0]}" not in "0" or "1"',log_args)

        if self.batch_items[-1].batch_status == BATCH_STATUS[1]: #'Running'
            self.batch_items[-1].complete_batch_item()

    def return_scan_time(self):
        """验证vessel中的记录的时间逻辑是否合理，返回soe扫描的起始时间
        rtn: (rslt_order, rslt_time)
        - ('match', <datetime>last_scan_time)
        - ('last_log_early', <datetime>last_scan_time)
        - ('batch_item_early', <datetime>batch_end_time/batch_start_time
        - ('no_log', None)"""
        assert isinstance(self.last_scan, Vessel_Last_Scan)
        last_scan_time = frac_to_msec(self.last_scan.last_log_time, self.last_scan.last_log_frac_sec) #
        if len(self.batch_items) > 0:
            last_batch = self.batch_items[-1]
        else:
            last_batch = None
        if isinstance(last_batch, Batch_Item):
            assert isinstance(last_batch.batch_start_time, datetime)
            if isinstance(last_batch.batch_end_time, datetime):
                assert last_batch.batch_end_time > last_batch.batch_start_time
                assert self.last_scan.last_batch_status != BATCH_STATUS[1] #Running
                if last_scan_time == last_batch.batch_end_time:
                    rslt_time = last_scan_time #将之前扫入的最后条log的时间作为返回结果（部分），供新的SOE扫描开始时间（调整前）
                    rslt_order = TIME_STAMP_ORDER[0] #match
                else:
                    if last_scan_time < last_batch.batch_end_time:
                        rslt_time = last_scan_time
                        rslt_order = TIME_STAMP_ORDER[2] #last_log_early
                    else:
                        rslt_time = last_batch.batch_end_time
                        rslt_order = TIME_STAMP_ORDER[1] #batch_item_early
            else: #没有batch_end_time
                assert self.last_scan.last_batch_status != BATCH_STATUS[2] #Completed
                if last_scan_time == last_batch.batch_start_time:
                    rslt_time = last_scan_time #将之前扫入的最后条log的时间作为返回结果（部分），供新的SOE扫描开始时间（调整前）
                    rslt_order = TIME_STAMP_ORDER[0] #match
                else:
                    if last_scan_time < last_batch.batch_end_time:
                        rslt_time = last_scan_time
                        rslt_order = TIME_STAMP_ORDER[2] #last_log_early
                    else:
                        rslt_time = last_batch.batch_start_time
                        rslt_order = TIME_STAMP_ORDER[1] #batch_item_early
        else:
            rslt_time = None
            rslt_order = TIME_STAMP_ORDER[3] #no_log
        result = (rslt_order, rslt_time)
        log_args = [rslt_order, rslt_time, self.vessel_no]
        add_log(40, "fn:valid_log_time return. '{0[2]}' rslt_order:'{0[0]}' rslt_time:'{0[1]}'", log_args)
        if logable(40):
            log_print("--------fn: valid_log_time() start--------")
            try:
                log_print("last_scan_time: {}".format(dt_to_string(last_scan_time)))
                log_print("last_batch_start_time: {}".format(dt_to_string(last_batch.batch_start_time)))
                log_print("last_batch_end_time: {}".format(dt_to_string(last_batch.batch_end_time)))
            except:
                add_log(30, "fn:valid_log_time(), exccept when print log")
            log_print("--------fn: valid_log_time() end--------")
        return result

    def update_last_scan(self):
        """update vessel.last_scan fields"""
        if len(self.batch_items) > 0:
            self.last_scan.last_batch_status = self.batch_items[-1].batch_status
            if self.last_scan.last_batch_status != BATCH_STATUS[2]: #'Complete'
                _last_log_time = self.batch_items[-1].batch_start_time
            else:
                _last_log_time = self.batch_items[-1].batch_end_time
            self.last_scan.last_log_time,self.last_scan.last_log_frac_sec = dtmsec_to_dt_and_frac(_last_log_time)
        log_args = [self.last_scan.last_batch_status,self.last_scan.last_log_time,self.last_scan.last_log_frac_sec]
        add_log(30,'[fn]update_last_scan:.batch_statuse="{0[0]}", .last_log_time="{0[1]}", .last_log_frac_sec="{0[2]}"', log_args)

    def dump_vessel_last_scan(self):
        """将vessel.last_scan结果导出文件
        vessel_last_scan: vessel.last_scan"""
        surfix = VESSEL_LAST_SCAN_SURFIX
        if isinstance(self.last_scan, Vessel_Last_Scan):
            _obj = self.last_scan
            serializing(_obj, DEF_PACKED_PATH + self.vessel_no + surfix)
        else:
            log_args = [self.last_scan]
            add_log(10, "fn:dump_vessel_last_scan. obj '{0[0]}' is not instance of Vessel.Last_Scan", log_args)

    def load_vessel_last_scan(self):
        """从文件或以默认初始值，加载前次扫描的Vessel_Last_Scan状态
        -init = True 以默认初始值载入， False从文件载入"""

        surfix = VESSEL_LAST_SCAN_SURFIX
        result = load(DEF_PACKED_PATH + self.vessel_no + surfix)

        add_log(40, "fn:load_vessel_last_scan() -return start---------------------")
        if logable(40) and result:
            #log_print("result.vessel_no: {}".format(result.vessel_no))
            log_print("result.last_batch_status: {}".format(result.last_batch_status))
            log_print("result.last_log_time: {}".format(result.last_log_time))
            log_print("result.last_log_frac_sec: {}".format(result.last_log_frac_sec))
        add_log(40, "fn:load_vessel_last_scan() -return end---------------------")
        return result

    def dump_vessel_batch_items(self):
        """将该vessel的批次摘要导出到文件"""
        surfix = VESSEL_BATCH_ITEMS_SURFIX
        serializing(self.batch_items, DEF_PACKED_PATH + self.vessel_no + surfix)

    def load_vessel_batch_items(self):
        """从文件或以默认初始值，加载batch_item"""
        surfix = VESSEL_BATCH_ITEMS_SURFIX
        result = load(DEF_PACKED_PATH + self.vessel_no + surfix)
        if not result:
            result = []
        return result

    def print_vessel_last_scan(self):
        log_print("[fn]Vessel.print_vessel_last_scan()------start------")
        log_print("vessel_no: {}".format(self.vessel_no))
        log_print("last_batch_status: {}".format(self.last_scan.last_batch_status))
        log_print("last_log_time: {}".format(self.last_scan.last_log_time))
        log_print("last_log_frac_sec: {}".format(self.last_scan.last_log_frac_sec))
        log_print("[fn]Vessel.print_vessel_last_scan()------end------")

    def print_batch_items(self):
        log_print("[fn]Vessel.print_batch_items()------start------")
        i = 0
        log_print("   #: Vessel     Batch_ID         Status             Start                       End                    Duration        Operation")
        for batch in self.batch_items:
            i += 1
            start_time = dt_f_to_string(utc_to_local(batch.batch_start_time))
            if isinstance(batch.batch_end_time,datetime):
                end_time = dt_f_to_string(utc_to_local(batch.batch_end_time))
            else:
                if batch.batch_status == BATCH_STATUS[1]: #'Running'
                    end_time = '--now--'
                else:
                    end_time = '--unkonwn--'
            duration = str(batch.duration)[:-7]
            #log_print("	{:0>4d}:{:x<8d}  {:x<10d}  {}".format(i,batch.vessel_no,batch.batch_status,start_time))
            log_print("{:>4d}: {:<10} {:<16} {:<10} {:<24}    {:<24} {:>16}      {:<16} ".format(i,batch.vessel_no,batch.batch_id,batch.batch_status,start_time,end_time,duration,batch.operation))
        log_print("[fn]Vessel.print_batch_items()------end------")

class SOE_Scan_Rslt():
    """扫描后批次定义的结果"""
    def __init__(self):
        self.first_log_time = None #过滤出的第一条SOE的时间UTC
        self.first_log_frac_sec = None #过滤出的第一条SOE的frac_sec
        self.last_log_time = None #过滤出的最后一条SOE的时间UTC
        self.last_log_frac_sec = None #过滤出的最后一条SOE的frac_sec
        self.batches_list = [] #存放Batch_Item

class Vessel_Last_Scan():
    """扫描后特定设备的状态"""
    def __init__(self):
        self.vessel_no = None
        self.last_batch_status = BATCH_STATUS[0]
        self.last_log_time_s = None #过滤出的最后一条SOE的时间UTC in string
        self.last_log_frac_sec = None #过滤出的最后一条SOE的frac_sec in int
        self.last_log_time = None #过滤出的最后一条SOE的时间UTC in <datetime>

class Batch_Item():
    """一个批次的记录概要"""
    def __init__(self):
        self.vessel_no = None
        self.batch_start_time = None #UTC in datetime
        self.batch_end_time = None #UTC in datetime
        self.duration = None
        self.batch_id = None
        self.operation = ''
        self.batch_status = BATCH_STATUS[0]
        self.comment = ''

    def complete_batch_item(self):
        """fill the fields of vessel.batch_items[item,...]"""
        def last_valid_value(batch_id_logs):
            """reverse order value_log validate.
            -return:
            -batch_id_logs: <[value_log,...]>"""
            for log in reversed(batch_id_logs):
                if valid_batch_id(log.value) != '--none--':
                    result = log.value.strip()
                    return result
            return '--none--'

        #complete duration
        if isinstance(self.batch_end_time,datetime):
            self.duration = self.batch_end_time - self.batch_start_time
            dt = self.batch_end_time
        else:
            self.duration = datetime.utcnow() - self.batch_start_time #handle running batch
            dt = datetime.utcnow()

        #complete batch_id
        item_id = self.vessel_no + r"-COMMON/BATCH_ID.CV"
        element_tree = create_raw_1pt_xml(dt,item_id)
        xml_path = XML_CONSTANT['raw_1pt']['xml_path']
        generate_xml(element_tree,xml_path)
        element_tree = None
        execute_xml(xml_path)
        result_path = XML_CONSTANT['raw_1pt']['result_path']
        batch_id = read_1pt(result_path)
        if valid_batch_id(batch_id.value) != '--none--':
            self.batch_id = batch_id.value.strip()
        else:
            start_time = self.batch_start_time
            end_time = self.batch_end_time
            element_tree = create_raw_mpt_xml(start_time,end_time,item_id)
            xml_path = XML_CONSTANT['raw_mpt']['xml_path']
            generate_xml(element_tree,xml_path)
            element_tree = None
            execute_xml(xml_path)
            result_path = XML_CONSTANT['raw_mpt']['result_path']
            batch_id_logs = read_mpt(result_path)
            self.batch_id = last_valid_value(batch_id_logs)

        #complete operation
        item_id = self.vessel_no + r"-COMMON/OPERATION.CV"
        element_tree = create_raw_1pt_xml(dt,item_id)
        xml_path = XML_CONSTANT['raw_1pt']['xml_path']
        generate_xml(element_tree,xml_path)
        element_tree = None
        execute_xml(xml_path)
        result_path = XML_CONSTANT['raw_1pt']['result_path']
        operation = read_1pt(result_path)
        if valid_batch_id(operation.value) != '--none--':
            self.operation = operation.value.strip()
        else:
            start_time = self.batch_start_time
            end_time = self.batch_end_time
            element_tree = create_raw_mpt_xml(start_time,end_time,item_id)
            xml_path = XML_CONSTANT['raw_mpt']['xml_path']
            generate_xml(element_tree,xml_path)
            element_tree = None
            execute_xml(xml_path)
            result_path = XML_CONSTANT['raw_mpt']['result_path']
            operation_logs = read_mpt(result_path)
            self.operation = last_valid_value(operation_logs)

    def print_batch_item(self):
        log_print("[fn]Batch_Item.print_batch_item():------start------")
        log_print("vessel_no: {}".format(self.vessel_no))
        log_print("batch_id: {}".format(self.batch_id))
        log_print("operation: {}".format(self.operation))
        log_print("batch_status: {}".format(self.batch_status))
        log_print("batch_start_time: {}".format(self.batch_start_time))
        log_print("batch_end_time: {}".format(self.batch_end_time))
        log_print("batch_duration: {}".format(self.batch_duration))
        log_print("comment: {}".format(self.comment))
        log_print("[fn]Batch_Item.print_batch_item():------end------")

class Soe_Db_Profile():
    """一条关于一个SOE DB起止时间的记录"""
    def __init__(self, db_name):
        self.db_name = db_name #in <str> e.g.
        self.db_start_time = None #UTC in datetime
        self.db_end_time = None #UTC in datetime
        self.query_time_span()

        log_args = [self.db_name]
        add_log(30, 'Soe_Db_Profile.db_name: {0[0]}', log_args)
        log_args = [self.db_start_time]
        add_log(30, 'Soe_Db_Profile.db_start_time: {0[0]}', log_args)
        log_args = [self.db_end_time]
        add_log(30, 'Soe_Db_Profile.db_end_time: {0[0]}', log_args)

    def query_time_span(self):
        #获取所含记录第一条及最后一条的时间戳
        dv_soe = DV_SOE(db=self.db_name)
        sql = r"select Top 1 Journal.Date_Time, Journal.FracSec From Journal"
        _start = dv_soe.enquiry(sql)[0]
        self.db_start_time = frac_to_msec(_start[0],_start[1])

        sql = (r"select Top 1 Journal.Date_Time, Journal.FracSec From Journal "
               r"ORDER BY Ord DESC")
        _end = dv_soe.enquiry(sql)[0]
        self.db_end_time = frac_to_msec(_end[0],_end[1])

        dv_soe.close()
        dv_soe = None

""" #not used?
class Batch_Start_Log():
    def __init__(self):
        self.batch_start = None #<0 or 1>
        self.date_time = None #<?>
        self.fracsec = None #<?>
"""

'''
future function
class Comments():
    """comments container"""
    def __init__(self):

    self.container = []
class Comment():
    def __init__(self):
        self.content = None
        self.by_account = None
        self.date_time = None #UTC
'''

def except_hook(cls, exception, traceback):
    """不明觉厉的找回traceback方法"""
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    app.aboutToQuit.connect(main.on_exit) #放程序退出前的必要动作
    main.show()
    sys.exit(app.exec_())
