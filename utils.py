
def read_cfg_file(config_filepath):
    """
    Convert all config sections to have unique names.
    |-Parameters
    | config_filepath | str |
    |-Return
    | cfg_parser| configparser.ConfigParser |
    |-Ref
    | https://github.com/qqwweee/keras-yolo3/blob/e6598d13c703029b2686bc2eb8d5c09badf42992/convert.py
    """
    import collections
    import io
    import configparser
    # [defaultdict の 利用 - Python defaultdict の使い方 - Qiita](https://qiita.com/xza/items/72a1b07fcf64d1f4bdb7#defaultdict-%E3%81%AE-%E5%88%A9%E7%94%A8)
    section_counters = collections.defaultdict(int)  # defaultdictは関数でdictのvalueを初期化

    output_stream = io.StringIO()
    with open(config_filepath) as fin:
        for line in fin:
            if line.startswith('['):
                section = line.strip().strip('[]')
                _section = section + '_' + str(section_counters[section])
                section_counters[section] += 1
                line = line.replace(section, _section)
            output_stream.write(line)
    output_stream.seek(0)

    cfg_parser = configparser.ConfigParser()
    cfg_parser.read_file(f=output_stream)
    return cfg_parser

def split_layer_structure(config_parser):
    """
    |-Return
    | structure_list | [features, scale_0, scale_1, scale_2]
    |                |
    |                | ex) [OrderedDict((section, configparser.SectionProxy),
    |                |                  (section, configparser.SectionProxy),
    |                |                  (section, configparser.SectionProxy)),
    |                |      OrderedDict((section, configparser.SectionProxy),
    |                |                  (section, configparser.SectionProxy),
    |                |                  (section, configparser.SectionProxy)),
    |                |      OrderedDict((section, configparser.SectionProxy)),
    |                |      OrderedDict((section, configparser.SectionProxy))]
    """
    import collections
    structure_list = [collections.OrderedDict()]
    idx = 0
    for section in cfg_parser.sections():
        if section == "scale_0" or section == "scale_1" or section == "scale_2":
            structure_list.append(collections.OrderedDict())
            idx += 1
            continue
        structure_list[idx][section] = cfg_parser[section]
    return structure_list
