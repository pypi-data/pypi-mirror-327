from configparser import ConfigParser


class RWConf:
    def __init__(self, filepath=None):
        """初始化一个配置文件"""
        self.cf = ConfigParser()
        self.cf.read(filepath, encoding='utf-8')

    def get_value(self, section, option):
        """获取配置文件section下的option的值，返回str类型"""
        return self.cf.get(section, option)

    def get_int(self, section, option):
        """获取配置文件section下的option的值，返回int类型"""
        return self.cf.getint(section, option)

    def get_float(self, section, option):
        """获取配置文件section下的option的值，返回float类型"""
        return self.cf.getfloat(section, option)

    def get_bool(self, section, option):
        """获取配置文件section下的option的值，返回bool类型"""
        return self.cf.getboolean(section, option)

    def get_value_eval(self, section, option):
        """获取配置文件section下的option的值，返回数据原类型"""
        return eval(self.cf.get(section, option))

    def set_value(self, section, option, value):
        self.cf.set(section, option, value)

    def write_file(self, filepath):
        with open(filepath, 'w+') as file:
            self.cf.write(file)


if __name__ == '__main__':
    import os
    root_path = os.path.dirname(os.path.realpath(__file__))
    print(root_path)
    conf_path = os.path.dirname(os.path.realpath(__file__)) + "\\conf.ini"
    print(conf_path)
    # read_conf = RWConf(filepath=conf_path)
    # pega_last_date = read_conf.get_value("base", "last_update_id")
    # print(pega_last_date)
    # read_conf.set_value("base", "last_update_id", "722611130")
    # read_conf.write_file(conf_path)
    # pti_last_date = read_conf.get_value("base", "last_update_id")
    # print(pti_last_date)
