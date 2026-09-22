#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anime_characters.py — IELTS Dopamine OS 角色数据库
====================================================
收录 147 名动漫/游戏经典角色：
  五星 47 名 | 四星 73 名 | 三星 27 名

[说明]
- 角色技能（ability/ultimate）全部还原原作，不含任何学习/XP 数值
- 五星大招、四星技能由下方代码从角色数据自动生成，抽到角色即同步获得
- 角色小课堂词汇（CHAR_VOCABULARY）保留双语例句，未收录角色回退通用词库
"""

# ============================================================
# 五星角色（47）
# ============================================================
FIVE_STAR_CHARS = {
    "luffy": {"name": "蒙奇·D·路飞", "anime": "海贼王", "element": "草帽一伙", "rarity": 5, "title": "未来的海贼王", "desc": "橡胶果实能力者，草帽一伙船长。要让四海成为最自由的海。", "ability": "橡胶果实·五档觉醒", "ultimate": "五档·猿神枪", "wish_text": "「海贼王，我当定了！」"},
    "naruto": {"name": "漩涡鸣人", "anime": "火影忍者", "element": "木叶七代目火影", "rarity": 5, "title": "九尾人柱力", "desc": "从吊车尾到七代目火影，靠的是永不言弃的忍道。", "ability": "九尾查克拉·六道仙人模式", "ultimate": "六道·尾兽玉螺旋手里剑", "wish_text": "「我从不收回说过的话，这就是我的忍道！」"},
    "goku": {"name": "孙悟空", "anime": "龙珠", "element": "赛亚人", "rarity": 5, "title": "宇宙最强战士", "desc": "不断突破极限的战斗天才，为变强而生的赛亚人。", "ability": "自在极意功", "ultimate": "自在极意·完美龟派气功", "wish_text": "「我还能变得更强！」"},
    "ichigo": {"name": "黑崎一护", "anime": "死神", "element": "死神代理", "rarity": 5, "title": "代理死神", "desc": "同时拥有死神、虚、灭却师三重力量的替代死神。", "ability": "死神·虚·灭却师三重力量", "ultimate": "虚化卍解·月牙天冲", "wish_text": "「我要保护我能保护的一切！」"},
    "tanjiro": {"name": "灶门炭治郎", "anime": "鬼灭之刃", "element": "鬼杀队", "rarity": 5, "title": "赫灼之子", "desc": "善良温柔的剑士，为拯救变成鬼的妹妹而战。", "ability": "全集中呼吸·日之呼吸", "ultimate": "火之神神乐·圆舞", "wish_text": "「纵使我身形俱灭，也定将恶鬼斩杀！」"},
    "eren": {"name": "艾伦·耶格尔", "anime": "进击的巨人", "element": "调查兵团", "rarity": 5, "title": "进击的巨人", "desc": "追求自由的战士，同时拥有进击与始祖巨人之力。", "ability": "进击的巨人·始祖巨人之力", "ultimate": "地鸣", "wish_text": "「把墙那边的敌人，一只不留地驱逐出去！」"},
    "gojo": {"name": "五条悟", "anime": "咒术回战", "element": "东京咒术高专", "rarity": 5, "title": "最强咒术师", "desc": "六眼与无下限术式的持有者，现代最强。", "ability": "六眼·无下限术式", "ultimate": "领域展开·无量空处", "wish_text": "「因为我最强，所以我没问题。」"},
    "gon": {"name": "小杰·富力士", "anime": "全职猎人", "element": "猎人协会", "rarity": 5, "title": "强化系天才", "desc": "寻找父亲的少年猎人，拥有惊人的成长潜力。", "ability": "强化系念能力", "ultimate": "猜猜拳·石头（制约与誓约）", "wish_text": "「我想知道自己能做到什么程度！」"},
    "edward": {"name": "爱德华·艾尔利克", "anime": "钢之炼金术师", "element": "国家炼金术师", "rarity": 5, "title": "钢之炼金术师", "desc": "最年轻的国家炼金术师，信条是等价交换。", "ability": "无需炼成阵的炼金术", "ultimate": "人体炼成·真理之门", "wish_text": "「等价交换！我的人生给你一半！」"},
    "conan": {"name": "江户川柯南", "anime": "名侦探柯南", "element": "帝丹小学", "rarity": 5, "title": "沉睡的小五郎", "desc": "被APTX4869缩小的名侦探工藤新一。", "ability": "超群的推理与运动神经", "ultimate": "麻醉针·沉睡的小五郎推理秀", "wish_text": "「真相只有一个！」"},
    "gintoki": {"name": "坂田银时", "anime": "银魂", "element": "万事屋", "rarity": 5, "title": "白夜叉", "desc": "攘夷战争的白夜叉，如今是吊儿郎当的万事屋老板。", "ability": "白夜叉的剑术", "ultimate": "白夜叉·洞爷湖真剑", "wish_text": "「就算崩溃也没关系，重新站起来就行。」"},
    "sakuragi": {"name": "樱木花道", "anime": "灌篮高手", "element": "湘北高中", "rarity": 5, "title": "天才篮球手", "desc": "自称天才的红发大前锋，篮板球之王。", "ability": "天才的身体素质与篮板直觉", "ultimate": "天才灌篮·制空权", "wish_text": "「我是天才！哈哈哈！」"},
    "shinji": {"name": "碇真嗣", "anime": "新世纪福音战士", "element": "NERV", "rarity": 5, "title": "第三适格者", "desc": "EVA初号机驾驶员，在挣扎与逃避中成长。", "ability": "EVA初号机·高同步率", "ultimate": "初号机·暴走", "wish_text": "「不能逃避，不能逃避，不能逃避！」"},
    "kirito": {"name": "桐谷和人", "anime": "刀剑神域", "element": "攻略组", "rarity": 5, "title": "黑色剑士", "desc": "SAO的封测玩家，唯一持有二刀流的剑士。", "ability": "独有技能·二刀流", "ultimate": "二刀流·星爆气流斩", "wish_text": "「在这个世界里，活下去就是胜利。」"},
    "saitama": {"name": "埼玉", "anime": "一拳超人", "element": "英雄协会", "rarity": 5, "title": "无敌的英雄", "desc": "每天100俯卧撑坚持三年，成为了一拳解决一切的英雄。", "ability": "无限的力量", "ultimate": "认真系列·认真拳", "wish_text": "「我只是一个兴趣使然的英雄。」"},
    "lelouch": {"name": "鲁路修·兰佩路基", "anime": "Code Geass", "element": "黑色骑士团", "rarity": 5, "title": "ZERO", "desc": "以Geass与谋略向帝国复仇的王子。", "ability": "Geass·绝对服从", "ultimate": "ZERO·黑色骑士团总司令", "wish_text": "「只有有被射杀觉悟的人，才有资格开枪。」"},
    "shirou": {"name": "卫宫士郎", "anime": "Fate/stay night", "element": "卫宫家", "rarity": 5, "title": "正义的伙伴", "desc": "业余魔术师，梦想成为正义的伙伴。", "ability": "投影魔术", "ultimate": "无限剑制·固有结界", "wish_text": "「I am the bone of my sword.」"},
    "tsuna": {"name": "沢田纲吉", "anime": "家庭教师", "element": "彭格列家族", "rarity": 5, "title": "第十代首领候补", "desc": "从废柴纲吉蜕变为彭格列第十代首领。", "ability": "死气之火·超直感", "ultimate": "X手套·超死气模式", "wish_text": "「我要保护我的家族！」"},
    "natsu": {"name": "纳兹·多拉格尼尔", "anime": "妖精的尾巴", "element": "妖精尾巴公会", "rarity": 5, "title": "火龙", "desc": "被火龙养大的灭龙魔导士，公会至上。", "ability": "灭龙魔法·火之灭龙", "ultimate": "灭龙奥义·红莲爆炎刃", "wish_text": "「我现在充满力量了！燃烧起来了！」"},
    "jotaro": {"name": "空条承太郎", "anime": "JOJO的奇妙冒险", "element": "星尘斗士", "rarity": 5, "title": "白金之星", "desc": "第三部主角，沉默寡言的高中生替身使者。", "ability": "替身·白金之星（力量·速度·精密）", "ultimate": "白金之星·欧拉欧拉连打", "wish_text": "「やれやれだぜ（真是够了）。」"},
    "giorno": {"name": "乔鲁诺·乔巴拿", "anime": "JOJO黄金之风", "element": "布加拉提小队", "rarity": 5, "title": "黄金体验", "desc": "DIO之子却怀有黄金精神，梦想成为流氓巨星。", "ability": "替身·黄金体验（赋予生命）", "ultimate": "黄金体验镇魂曲", "wish_text": "「我，乔鲁诺·乔巴拿，有一个梦想。」"},
    "dio": {"name": "DIO", "anime": "JOJO的奇妙冒险", "element": "吸血鬼·替身使者", "rarity": 5, "title": "世界的DIO", "desc": "野心与生命力都超越人类的恶之帝王。", "ability": "替身·世界（时间停止）与吸血鬼体质", "ultimate": "THE WORLD·时间停止", "wish_text": "「砸瓦鲁多！时间是属于我的！」"},
    "itachi": {"name": "宇智波鼬", "anime": "火影忍者", "element": "晓", "rarity": 5, "title": "背负一切的天才", "desc": "以一人之身背负木叶与弟弟未来的天才忍者。", "ability": "万花筒写轮眼", "ultimate": "天照·月读·须佐能乎", "wish_text": "「原谅我，佐助，这是最后一次了。」"},
    "jiraiya": {"name": "自来也", "anime": "火影忍者", "element": "传说中的三忍", "rarity": 5, "title": "蛤蟆仙人", "desc": "豪放不羁的仙人，鸣人一生的导师。", "ability": "仙术·螺旋丸", "ultimate": "仙人模式·超大玉螺旋丸", "wish_text": "「忍者的本分就是永不放弃！」"},
    "ace": {"name": "波特卡斯·D·艾斯", "anime": "海贼王", "element": "白胡子海贼团", "rarity": 5, "title": "火拳", "desc": "路飞的义兄，用燃烧的拳头回报这个否定他的世界。", "ability": "烧烧果实", "ultimate": "大炎戒·炎帝", "wish_text": "「谢谢你爱我。」"},
    "shanks": {"name": "红发香克斯", "anime": "海贼王", "element": "红发海贼团", "rarity": 5, "title": "四皇", "desc": "把草帽托付给路飞的自由海贼，四皇之一。", "ability": "顶尖霸气", "ultimate": "四皇的霸王色", "wish_text": "「这顶草帽，就托付给你了。」"},
    "aizen": {"name": "蓝染惣右介", "anime": "死神", "element": "护廷十三队·虚圈", "rarity": 5, "title": "镜花水月", "desc": "以温柔面具隐藏野心的最强叛逃者。", "ability": "镜花水月（完全催眠）", "ultimate": "崩玉融合·无月", "wish_text": "「仰慕是距离理解最遥远的东西。」"},
    "frieza": {"name": "弗利萨", "anime": "龙珠", "element": "弗利萨军团", "rarity": 5, "title": "宇宙帝王", "desc": "天生的战斗天才，冷酷优雅的宇宙霸主。", "ability": "多段变身·恐怖战斗天赋", "ultimate": "死亡光束·最终形态", "wish_text": "「我要把你变成宇宙的尘埃。」"},
    "kid": {"name": "怪盗基德", "anime": "名侦探柯南", "element": "怪盗", "rarity": 5, "title": "月下的魔术师", "desc": "1412号怪盗，在月光下用魔术寻找潘多拉宝石。", "ability": "变装与魔术手法", "ultimate": "月光下的魔术表演", "wish_text": "「怪盗是华丽盗取的创造性艺术家。」"},
    "rengoku": {"name": "炼狱杏寿郎", "anime": "鬼灭之刃", "element": "鬼杀队·炎柱", "rarity": 5, "title": "炎柱", "desc": "豪迈燃烧的炎柱，绝不会让任何人死去。", "ability": "全集中呼吸·炎之呼吸", "ultimate": "炎之呼吸·奥义·炼狱", "wish_text": "「我会履行职责，不叫任何人死去！」"},
    "muzan": {"name": "鬼舞辻无惨", "anime": "鬼灭之刃", "element": "十二鬼月·始祖", "rarity": 5, "title": "千年鬼王", "desc": "所有鬼的始祖，惧怕死亡的完美主义者。", "ability": "细胞支配·千年鬼力", "ultimate": "十二鬼月·血鬼术", "wish_text": "「我可是完美的生物。」"},
    "sukuna": {"name": "两面宿傩", "anime": "咒术回战", "element": "诅咒之王", "rarity": 5, "title": "千年前的最强咒术师", "desc": "寄宿在虎杖体内的诅咒之王，二十根手指的力量。", "ability": "宿傩之力·御厨子", "ultimate": "伏魔御厨子·解与捌", "wish_text": "「朕，即是诅咒之王。」"},
    "erwin": {"name": "埃尔文·史密斯", "anime": "进击的巨人", "element": "调查兵团", "rarity": 5, "title": "团长", "desc": "把生命献给人类未来的调查兵团团长。", "ability": "卓越的战略与献身", "ultimate": "献出心脏·总攻冲锋", "wish_text": "「献出你们的心脏！」"},
    "saber": {"name": "阿尔托莉雅·潘德拉贡", "anime": "Fate/stay night", "element": "骑士王", "rarity": 5, "title": "Saber", "desc": "不列颠的骑士王，以圣剑之名参战的从者。", "ability": "对魔力·圣剑使", "ultimate": "誓约胜利之剑·Excalibur", "wish_text": "「问汝：汝为人否？」"},
    "gilgamesh": {"name": "吉尔伽美什", "anime": "Fate/stay night", "element": "英雄王", "rarity": 5, "title": "Archer", "desc": "最古老的英雄王，收藏了人类一切财宝。", "ability": "王之财宝", "ultimate": "天地乖离·开辟之星", "wish_text": "「杂种，记得仰望本王。」"},
    "reborn": {"name": "里包恩", "anime": "家庭教师", "element": "彭格列·彩虹之子", "rarity": 5, "title": "世界第一杀手", "desc": "受命培养第十代首领的婴儿杀手家庭教师。", "ability": "世界最强杀手·死气之炎", "ultimate": "列恩变形·死气弹", "wish_text": "「Ciaossu，我是家庭教师里包恩。」"},
    "l": {"name": "L·罗莱特", "anime": "死亡笔记", "element": "ICPO特别顾问", "rarity": 5, "title": "世界第一侦探", "desc": "以怪异姿势与海量甜食支撑推理的传奇侦探。", "ability": "世界第一的推理", "ultimate": "全球监视与推理网", "wish_text": "「正义必胜……我是正义。」"},
    "all_might": {"name": "欧尔麦特", "anime": "我的英雄学院", "element": "NO.1英雄", "rarity": 5, "title": "和平的象征", "desc": "以笑容守护世界的NO.1英雄，One For All第八代继承者。", "ability": "One For All", "ultimate": "United Smash", "wish_text": "「已经不要紧了。为什么？因为我来了！」"},
    "makima": {"name": "玛奇玛", "anime": "链锯人", "element": "公安对魔特异课", "rarity": 5, "title": "支配之恶魔", "desc": "温柔微笑下藏着支配一切的恶魔本相。", "ability": "支配之恶魔", "ultimate": "支配·万灵服从", "wish_text": "「狗要听主人的话哦。」"},
    "kaneki": {"name": "金木研", "anime": "东京喰种", "element": "半喰种", "rarity": 5, "title": "百日战王? 不——百年喰种", "desc": "被变成半喰种的大学生，在痛苦中重生。", "ability": "赫子·超速再生", "ultimate": "半赫者·鳞赫暴走", "wish_text": "「1000减7等于多少？」"},
    "frieren": {"name": "芙莉莲", "anime": "葬送的芙莉莲", "element": "一级魔法使", "rarity": 5, "title": "千年魔法使", "desc": "活了千年的精灵魔法使，在人死后才开始了解人类。", "ability": "千年精灵魔法", "ultimate": "杀魔魔法·泽利耶之流", "wish_text": "「我只是想更多地了解人类。」"},
    "anya": {"name": "阿尼亚", "anime": "间谍过家家", "element": "伊甸学园", "rarity": 5, "title": "实验体007", "desc": "能读心的治愈系小萝莉，福杰家的和平担当。", "ability": "读心术", "ultimate": "作战「让爸爸妈妈相亲相爱」", "wish_text": "「哇酷哇酷！阿尼亚想要和平！」"},
    "pikachu": {"name": "皮卡丘", "anime": "宝可梦", "element": "电系宝可梦", "rarity": 5, "title": "电气鼠", "desc": "拒绝进精灵球的倔强宝可梦，小智永远的搭档。", "ability": "电气囊·十万伏特", "ultimate": "十万伏特", "wish_text": "「皮卡皮卡！」"},
    "yugi": {"name": "武藤游戏", "anime": "游戏王", "element": "决斗者", "rarity": 5, "title": "法老王的宿主", "desc": "解开封印之物的少年，与三千年前的法老王共享身体。", "ability": "千年积木·法老王", "ultimate": "奇迹的抽卡·黑魔术师", "wish_text": "「我的回合，抽卡！」"},
    "doraemon": {"name": "哆啦A梦", "anime": "哆啦A梦", "element": "22世纪猫型机器人", "rarity": 5, "title": "来自未来的蓝胖子", "desc": "被老鼠咬掉耳朵后怕老鼠的保姆机器人，口袋里装着未来。", "ability": "四次元口袋", "ultimate": "随意门·任意道具", "wish_text": "「大雄——！」"},
    "inuyasha": {"name": "犬夜叉", "anime": "犬夜叉", "element": "半妖", "rarity": 5, "title": "半妖少年", "desc": "人类与妖之间出生的半妖，挥舞铁碎牙斩尽妖魔。", "ability": "铁碎牙·妖力", "ultimate": "爆流破", "wish_text": "「我用铁碎牙劈了你！」"},
    "kenshin": {"name": "绯村剑心", "anime": "浪客剑心", "element": "流浪剑客", "rarity": 5, "title": "刽子手拔刀斋", "desc": "幕末最强刽子手，立誓此后不再杀人。", "ability": "飞天御剑流", "ultimate": "天翔龙闪", "wish_text": "「剑是凶器，剑术是杀人术。」"},
}

# ============================================================
# 四星角色（73）
# ============================================================
FOUR_STAR_CHARS = {
    "zoro": {"name": "罗罗诺亚·索隆", "anime": "海贼王", "element": "草帽一伙", "rarity": 4, "title": "海贼猎人", "desc": "三刀流剑士，路飞的第一个伙伴，方向感为零。", "ability": "三刀流剑术", "ultimate": "三千世界", "wish_text": "「我要成为世界第一的大剑豪！」"},
    "sanji": {"name": "山治", "anime": "海贼王", "element": "草帽一伙", "rarity": 4, "title": "黑足", "desc": "草帽团厨师，只用脚战斗的绅士。", "ability": "恶魔风脚", "ultimate": "魔神风脚", "wish_text": "「为了女士，我愿意做任何事！」"},
    "sasuke": {"name": "宇智波佐助", "anime": "火影忍者", "element": "木叶·晓", "rarity": 4, "title": "复仇者", "desc": "宇智波一族的幸存者，为复仇而修行。", "ability": "写轮眼·轮回眼", "ultimate": "须佐能乎·加具土命", "wish_text": "「我的道路，由我自己决定。」"},
    "kakashi": {"name": "旗木卡卡西", "anime": "火影忍者", "element": "木叶六代目火影", "rarity": 4, "title": "拷贝忍者", "desc": "复制过千种忍术的写轮眼卡卡西。", "ability": "复制忍者·雷切", "ultimate": "雷切·双雷震", "wish_text": "「我不会让我的同伴被杀。」"},
    "vegeta": {"name": "贝吉塔", "anime": "龙珠", "element": "赛亚人王子", "rarity": 4, "title": "赛亚人王子", "desc": "高傲的王子，永远在追赶卡卡罗特。", "ability": "超级赛亚人", "ultimate": "终极闪光", "wish_text": "「我可是赛亚人王子贝吉塔！」"},
    "rukia": {"name": "朽木露琪亚", "anime": "死神", "element": "护廷十三队", "rarity": 4, "title": "袖白雪", "desc": "把死神之力交给一护的死神，朽木家养女。", "ability": "斩魄刀·袖白雪", "ultimate": "卍解·白霞罚", "wish_text": "「我是朽木露琪亚，请多指教。」"},
    "nezuko": {"name": "灶门祢豆子", "anime": "鬼灭之刃", "element": "鬼杀队", "rarity": 4, "title": "鬼化的少女", "desc": "变成鬼却保有人心的少女，炭治郎的妹妹。", "ability": "血鬼术", "ultimate": "爆血", "wish_text": "「唔唔唔！（哥哥加油！）」"},
    "zenitsu": {"name": "我妻善逸", "anime": "鬼灭之刃", "element": "鬼杀队", "rarity": 4, "title": "雷之呼吸传人", "desc": "胆小如鼠，睡着后却是超一流的剑士。", "ability": "全集中呼吸·雷之呼吸", "ultimate": "霹雳一闪六连", "wish_text": "「我不想死啊——！（然后睡着了）」"},
    "levi": {"name": "利威尔·阿克曼", "anime": "进击的巨人", "element": "调查兵团", "rarity": 4, "title": "人类最强士兵", "desc": "人类最强士兵，有洁癖的兵团兵长。", "ability": "阿克曼之力·立体机动", "ultimate": "立体机动·旋风斩", "wish_text": "「放弃你的梦想，去死吧。」"},
    "itadori": {"name": "虎杖悠仁", "anime": "咒术回战", "element": "东京咒术高专", "rarity": 4, "title": "宿傩的容器", "desc": "吞下宿傩手指的少年，希望人们得到正确的死亡。", "ability": "超人体能·宿傩容器", "ultimate": "黑闪连打", "wish_text": "「我要让更多人得到正确的死亡！」"},
    "killua": {"name": "奇犽·揍敌客", "anime": "全职猎人", "element": "猎人协会", "rarity": 4, "title": "暗杀世家继承人", "desc": "暗杀世家出身的天才少年，小杰最好的朋友。", "ability": "变化系念能力·神速", "ultimate": "神速·电光火石", "wish_text": "「我要和小杰一起，走得更远。」"},
    "alphonse": {"name": "阿尔冯斯·艾尔利克", "anime": "钢之炼金术师", "element": "铠甲之魂", "rarity": 4, "title": "灵魂铠甲", "desc": "灵魂被封印在铠甲上的温柔少年。", "ability": "铠甲武斗术", "ultimate": "灵魂铠甲·巨拳", "wish_text": "「哥哥，我们一定能找回身体。」"},
    "haibara": {"name": "灰原哀", "anime": "名侦探柯南", "element": "前黑衣组织", "rarity": 4, "title": "APTX4869研究者", "desc": "研制缩小药水的天才科学家。", "ability": "科学头脑·药学", "ultimate": "APTX4869·科学分析", "wish_text": "「我只是觉得，你很有趣。」"},
    "light": {"name": "夜神月", "anime": "死亡笔记", "element": "Kira", "rarity": 4, "title": "新世界的神", "desc": "捡到死亡笔记的优等生，自称正义的神。", "ability": "死亡笔记·头脑战", "ultimate": "死亡笔记·写上名字", "wish_text": "「我要成为新世界的神！」"},
    "rukawa": {"name": "流川枫", "anime": "灌篮高手", "element": "湘北高中", "rarity": 4, "title": "超级新人", "desc": "湘北的王牌，冷酷的得分手。", "ability": "篮球天才·空中漫步", "ultimate": "飘逸上篮", "wish_text": "「……（沉默，然后进球）」"},
    "law": {"name": "特拉法尔加·罗", "anime": "海贼王", "element": "心脏海贼团", "rarity": 4, "title": "死亡外科医生", "desc": "手术果实能力者，能把战场变成手术室。", "ability": "手术果实·ROOM", "ultimate": "ROOM·屠宰场", "wish_text": "「ROOM——屠宰场！」"},
    "ayanami": {"name": "绫波丽", "anime": "新世纪福音战士", "element": "NERV", "rarity": 4, "title": "第一适格者", "desc": "零号机驾驶员，沉默寡言的蓝发少女。", "ability": "EVA零号机·AT力场", "ultimate": "AT力场展开", "wish_text": "「……我是谁？」"},
    "asuka": {"name": "惣流·明日香", "anime": "新世纪福音战士", "element": "NERV", "rarity": 4, "title": "第二适格者", "desc": "骄傲的天才少女，二号机驾驶员。", "ability": "EVA二号机·兽化", "ultimate": "二号机兽化模式", "wish_text": "「你是笨蛋吗？」"},
    "asuna": {"name": "亚丝娜", "anime": "刀剑神域", "element": "攻略组", "rarity": 4, "title": "闪光", "desc": "SAO攻略组核心，细剑的闪光。", "ability": "细剑·闪光", "ultimate": "星屑飞溅", "wish_text": "「我会一直陪在你身边。」"},
    "genos": {"name": "杰诺斯", "anime": "一拳超人", "element": "英雄协会", "rarity": 4, "title": "魔鬼改造人", "desc": "埼玉的弟子，全机械改造的S级英雄。", "ability": "改造人·焚烧炮", "ultimate": "焚烧炮·超螺旋", "wish_text": "「老师，请指教！」"},
    "cc": {"name": "C.C.", "anime": "Code Geass", "element": "不死的魔女", "rarity": 4, "title": "不死的魔女", "desc": "赋予Geass的不死魔女，披萨狂热爱好者。", "ability": "不死之身·Geass赋予", "ultimate": "Geass·契约之力", "wish_text": "「你知道吗？雪为什么是白色的？」"},
    "sakura_fate": {"name": "间桐樱", "anime": "Fate/stay night", "element": "间桐家", "rarity": 4, "title": "温柔的魔术师", "desc": "背负黑暗过去的温柔学妹。", "ability": "虚数魔术·影", "ultimate": "影之巨人", "wish_text": "「学长，欢迎回来。」"},
    "hibari": {"name": "云雀恭弥", "anime": "家庭教师", "element": "彭格列云之守护者", "rarity": 4, "title": "风纪委员长", "desc": "孤高的云之守护者，并盛中学的 biting kill。", "ability": "浮萍拐·云之属性", "ultimate": "咬杀", "wish_text": "「咬杀你。」"},
    "lucy": {"name": "露西·哈特菲利亚", "anime": "妖精的尾巴", "element": "妖精尾巴公会", "rarity": 4, "title": "星灵魔导士", "desc": "用星灵钥匙召唤黄道十二宫的魔导士。", "ability": "星灵魔法", "ultimate": "黄道十二门", "wish_text": "「我们是妖精的尾巴！」"},
    "erza": {"name": "艾露莎·舒卡勒托", "anime": "妖精的尾巴", "element": "妖精尾巴公会", "rarity": 4, "title": "妖精女王", "desc": "换装魔导士，一人在手百把剑。", "ability": "换装魔法·天伦之铠", "ultimate": "天伦之铠·幽绝", "wish_text": "「为了同伴，我可以变得更强！」"},
    "giyu": {"name": "富冈义勇", "anime": "鬼灭之刃", "element": "鬼杀队·水柱", "rarity": 4, "title": "水柱", "desc": "沉默寡言的水柱，斩鬼时的第十一型生生流转。", "ability": "全集中呼吸·水之呼吸", "ultimate": "生生流转", "wish_text": "「我没有被讨厌。」"},
    "joseph": {"name": "乔瑟夫·乔斯达", "anime": "JOJO的奇妙冒险", "element": "乔斯达家族", "rarity": 4, "title": "波纹与替身的二刀流", "desc": "狡猾又帅气的老油条乔斯达二世。", "ability": "波纹·紫色隐者之念", "ultimate": "你的下一句话是——", "wish_text": "「你的下一句话是：『我要抽卡』！」"},
    "kakyoin": {"name": "花京院典明", "anime": "JOJO的奇妙冒险", "element": "星尘斗士", "rarity": 4, "title": "法皇之绿", "desc": "以远程结界作战的高智商替身使者。", "ability": "替身·法皇之绿（远程结界）", "ultimate": "绿宝石水花", "wish_text": "「我的王牌，法皇之绿！」"},
    "yusuke": {"name": "浦饭幽助", "anime": "幽游白书", "element": "灵界侦探", "rarity": 4, "title": "不良少年侦探", "desc": "不良少年出身的灵界侦探，雷禅的血脉。", "ability": "灵丸·妖力", "ultimate": "灵丸·魔族觉醒", "wish_text": "「灵丸！」"},
    "hiei": {"name": "飞影", "anime": "幽游白书", "element": "冰河之国", "rarity": 4, "title": "邪眼剑客", "desc": "三尺短剑与邪眼，沉默的火焰妖。", "ability": "邪眼·居合剑术", "ultimate": "邪王炎杀黑龙波", "wish_text": "「哼，别挡我的路。」"},
    "hisoka": {"name": "西索", "anime": "全职猎人", "element": "幻影旅团", "rarity": 4, "title": "变幻系魔术师", "desc": "只对变强的猎物感兴趣的战斗狂魔术师。", "ability": "伸缩自如的爱", "ultimate": "轻薄的假象·戾桥", "wish_text": "「我等的就是这个时刻♪」"},
    "gaara": {"name": "我爱罗", "anime": "火影忍者", "element": "砂隐村风影", "rarity": 4, "title": "第五代风影", "desc": "从只爱自己到守护村子的砂之风影。", "ability": "砂之守护·一尾", "ultimate": "砂缚柩·守鹤之盾", "wish_text": "「我也想守护重要的伙伴。」"},
    "minato": {"name": "波风水门", "anime": "火影忍者", "element": "木叶四代目火影", "rarity": 4, "title": "金色闪光", "desc": "以飞雷神之名震动忍界的四代目火影。", "ability": "飞雷神之术·螺旋丸", "ultimate": "飞雷神二段·螺旋闪光", "wish_text": "「金色闪光，参上。」"},
    "byakuya": {"name": "朽木白哉", "anime": "死神", "element": "护廷十三队六番队", "rarity": 4, "title": "六番队队长", "desc": "贵族的最高典范，露琪亚的义兄。", "ability": "斩魄刀·千本樱景严", "ultimate": "歼景·千本樱景严", "wish_text": "「散落吧，千本樱景严。」"},
    "zaraki": {"name": "更木剑八", "anime": "死神", "element": "护廷十三队十一番队", "rarity": 4, "title": "剑八", "desc": "为战斗而生的十一番队队长。", "ability": "压倒性灵压·剑术", "ultimate": "始解·野晒", "wish_text": "「再强一点！让我更尽兴一点！」"},
    "ulquiorra": {"name": "乌尔奇奥拉·西法", "anime": "死神", "element": "虚圈·十刃", "rarity": 4, "title": "十刃第四", "desc": "追寻『心』为何物的虚无之刃。", "ability": "虚闪·归刃", "ultimate": "二段归刃·黑翼大魔", "wish_text": "「心，是什么？」"},
    "hitsugaya": {"name": "日番谷冬狮郎", "anime": "死神", "element": "护廷十三队十番队", "rarity": 4, "title": "天才少年队长", "desc": "最年少成为队长的冰之天才。", "ability": "斩魄刀·冰轮丸", "ultimate": "端坐于霜天·冰轮丸", "wish_text": "「端坐于霜天，冰轮丸。」"},
    "piccolo": {"name": "比克", "anime": "龙珠", "element": "那美克星人", "rarity": 4, "title": "大魔王", "desc": "从宿敌变成悟空家族最可靠的守护者。", "ability": "那美克星·再生与魔贯光杀炮", "ultimate": "魔贯光杀炮", "wish_text": "「这是那美克星人的骄傲。」"},
    "kagura": {"name": "神乐", "anime": "银魂", "element": "万事屋", "rarity": 4, "title": "夜兔族少女", "desc": "夜兔族的天才少女，饭量与战力成正比。", "ability": "夜兔族怪力·伞术", "ultimate": "夜兔之拳·阿鲁！", "wish_text": "「啊鲁！」"},
    "okita": {"name": "冲田总悟", "anime": "银魂", "element": "真选组一番队", "rarity": 4, "title": "真选组第一剑", "desc": "微笑着说狠话的真选组第一剑士。", "ability": "居合·火箭筒", "ultimate": "三段突刺", "wish_text": "「睡着的笨蛋，要被运走哦。」"},
    "hijikata": {"name": "土方十四郎", "anime": "银魂", "element": "真选组副长", "rarity": 4, "title": "鬼之副长", "desc": "严守局中法度的真选组鬼之副长。", "ability": "居合道·妖刀村麻纱", "ultimate": "鬼之副长·居合斩", "wish_text": "「真选组局中法度第五条——不许胡作非为。」"},
    "heiji": {"name": "服部平次", "anime": "名侦探柯南", "element": "大阪府警", "rarity": 4, "title": "关西的名侦探", "desc": "与新一齐名的西部高中生侦探。", "ability": "推理与剑道", "ultimate": "双雄推理对决", "wish_text": "「工藤新一，来决一胜负吧！」"},
    "akai": {"name": "赤井秀一", "anime": "名侦探柯南", "element": "FBI", "rarity": 4, "title": "银色的子弹", "desc": "狙击率超高的FBI搜查官，黑衣组织的噩梦。", "ability": "神级狙击", "ultimate": "银色的子弹", "wish_text": "「FBI，不许动。」"},
    "mitsui": {"name": "三井寿", "anime": "灌篮高手", "element": "湘北高中", "rarity": 4, "title": "回归的三分王", "desc": "误入歧途又归来的三分神射手。", "ability": "三分球·不屈斗志", "ultimate": "连发三分雨", "wish_text": "「教练，我想打篮球。」"},
    "sendoh": {"name": "仙道彰", "anime": "灌篮高手", "element": "陵南高中", "rarity": 4, "title": "陵南的王牌", "desc": "笑着打球的全能王牌，樱木最想超越的人。", "ability": "全能球风·大局观", "ultimate": "王牌的全面统治", "wish_text": "「陵南的王牌就是我。」"},
    "suzaku": {"name": "枢木朱雀", "anime": "Code Geass", "element": "布里塔尼亚军·圆桌骑士", "rarity": 4, "title": "白色死神", "desc": "驾驶兰斯洛特的白色骑士，想从内部改变帝国。", "ability": "骑士马术·兰斯洛特", "ultimate": "兰斯洛特·瓦利 takewhat? ——全领域机动", "wish_text": "「用正确的方法，改变这个世界。」"},
    "rin": {"name": "远坂凛", "anime": "Fate/stay night", "element": "远坂家", "rarity": 4, "title": "Tohsaka家传人", "desc": "完美淑女面具下的傲娇魔术师。", "ability": "宝石魔术", "ultimate": "宝石魔术·全弹发射", "wish_text": "「别误会，我才不是为了你呢！」"},
    "cu_chulainn": {"name": "库丘林", "anime": "Fate/stay night", "element": "凯尔特神话", "rarity": 4, "title": "Lancer", "desc": "凯尔特的光之子，最忠诚的枪兵。", "ability": "刺穿死棘之枪", "ultimate": "刺穿死翔之枪", "wish_text": "「痛快地打一场吧！」"},
    "gokudera": {"name": "狱寺隼人", "anime": "家庭教师", "element": "彭格列岚之守护者", "rarity": 4, "title": "炸弹狂", "desc": "自称十代目右腕的炸弹专家。", "ability": "炸药·岚之属性", "ultimate": "系统C.A.I.岚之炎", "wish_text": "「十代目，请让我跟随您！」"},
    "yamamoto": {"name": "山本武", "anime": "家庭教师", "element": "彭格列雨之守护者", "rarity": 4, "title": "时雨金时", "desc": "把杀伐当棒球的乐天派剑士。", "ability": "时雨金时·剑道", "ultimate": "时雨金时·一之太刀", "wish_text": "「剑道嘛，开心就好。」"},
    "mukuro": {"name": "六道骸", "anime": "家庭教师", "element": "雾之守护者", "rarity": 4, "title": "六道轮回", "desc": "蓝发的雾之守护者，掌控六道轮回之力。", "ability": "六道轮回·幻术", "ultimate": "六道轮回·地狱道", "wish_text": "「我要毁灭这个虚伪的世界。」"},
    "bang": {"name": "邦古", "anime": "一拳超人", "element": "英雄协会", "rarity": 4, "title": "银色獠牙", "desc": "流水岩碎拳的宗师，S级第三位的老武道家。", "ability": "流水岩碎拳", "ultimate": "流水岩碎拳·奥义", "wish_text": "「年轻人，学学怎么战斗吧。」"},
    "kaworu": {"name": "渚薰", "anime": "新世纪福音战士", "element": "NERV", "rarity": 4, "title": "第五适格者", "desc": "自由天使，最后把选择交给真嗣。", "ability": "自由同步率·AT力场", "ultimate": "天使之力·自我献身", "wish_text": "「我生来就是为了遇见你的。」"},
    "alice": {"name": "爱丽丝", "anime": "刀剑神域", "element": "整合骑士", "rarity": 4, "title": "整合骑士", "desc": "Underworld最高级AI，金桂之骑士。", "ability": "神圣术·整合骑士剑技", "ultimate": "金木犀之剑", "wish_text": "「整合骑士爱丽丝·辛赛西斯·萨蒂。」"},
    "sinon": {"name": "朝田诗乃", "anime": "刀剑神域", "element": "狙击手", "rarity": 4, "title": "冰之狙击手", "desc": "GGO的神狙击手，克服了枪的恐惧。", "ability": "狙击·Hecate II", "ultimate": "2700米超远程狙击", "wish_text": "「我不再是那个胆小的女孩了。」"},
    "gray": {"name": "格雷·佛尔巴斯特", "anime": "妖精的尾巴", "element": "妖精尾巴公会", "rarity": 4, "title": "冰之造型魔导士", "desc": "冰之造型魔导士，习惯性脱衣。", "ability": "冰之造型魔法", "ultimate": "冰刃七连舞", "wish_text": "「别误会！」"},
    "gajeel": {"name": "伽吉鲁", "anime": "妖精的尾巴", "element": "妖精尾巴公会", "rarity": 4, "title": "铁龙", "desc": "前幻影旅团? 不——前幽灵团的铁之灭龙魔导士。", "ability": "铁之灭龙魔法", "ultimate": "铁龙的咆哮", "wish_text": "「铁龙的咆哮！」"},
    "near": {"name": "尼亚", "anime": "死亡笔记", "element": "SPK", "rarity": 4, "title": "L的继承者", "desc": "与梅洛竞争L继承权的白发少年。", "ability": "推理·玩具方阵", "ultimate": "假笔记·完全陷阱", "wish_text": "「我不是L的继承者，我是Near。」"},
    "ryoma": {"name": "越前龙马", "anime": "网球王子", "element": "青春学园", "rarity": 4, "title": "网球王子", "desc": "自称还差得远的美式网球天才少年。", "ability": "Twist Serve·单脚小碎步", "ultimate": "COOL Drive", "wish_text": "「你还差得远呢。」"},
    "satoshi": {"name": "小智", "anime": "宝可梦", "element": "真新镇", "rarity": 4, "title": "阿罗拉冠军", "desc": "和皮卡丘一起走遍世界的少年训练家。", "ability": "羁绊进化", "ultimate": "十万伏特·羁绊一击", "wish_text": "「我要成为宝可梦大师！」"},
    "kaiba": {"name": "海马濑人", "anime": "游戏王", "element": "海马公司", "rarity": 4, "title": "青眼的持有者", "desc": "只为三张青眼白龙而活的决斗天才。", "ability": "商业帝国·决斗天赋", "ultimate": "青眼白龙·毁灭的爆裂弹", "wish_text": "「青眼白龙，毁灭光芒！」"},
    "deku": {"name": "绿谷出久", "anime": "我的英雄学院", "element": "雄英高中", "rarity": 4, "title": "无个性的少年", "desc": "继承One For All的analysis少年英雄。", "ability": "One For All继承·超分析", "ultimate": "One For All·Full Cowling", "wish_text": "「从今天起，这也是我的『个性』！」"},
    "bakugo": {"name": "爆豪胜己", "anime": "我的英雄学院", "element": "雄英高中", "rarity": 4, "title": "Kacchan", "desc": "以第一为唯一目标的爆破系天才。", "ability": "个性·爆破", "ultimate": "AP Shot", "wish_text": "「我要成为超越欧尔麦特的第一英雄！」"},
    "todoroki": {"name": "轰焦冻", "anime": "我的英雄学院", "element": "雄英高中", "rarity": 4, "title": "冰与火的王子", "desc": "继承父之火与母之冰的半冰半火天才。", "ability": "半冷半燃", "ultimate": "冰墙·天与地的界限", "wish_text": "「这是我自己选择的路。」"},
    "denji": {"name": "电次", "anime": "链锯人", "element": "公安对魔特异课", "rarity": 4, "title": "链锯人", "desc": "和链锯恶魔波奇塔融为一体的穷小子。", "ability": "链锯恶魔·心脏", "ultimate": "链锯启动·斩击全开", "wish_text": "「电锯人，登场！」"},
    "power": {"name": "帕瓦", "anime": "链锯人", "element": "公安对魔特异课", "rarity": 4, "title": "血之恶魔", "desc": "自恋又怕死的粗暴美人血之恶魔。", "ability": "血液武器化", "ultimate": "血之锤·千针", "wish_text": "「我是血之恶魔帕瓦！粗暴美人！」"},
    "shinobu": {"name": "蝴蝶忍", "anime": "鬼灭之刃", "element": "鬼杀队·虫柱", "rarity": 4, "title": "虫柱", "desc": "以毒代刃的微笑虫柱。", "ability": "虫之呼吸·毒素", "ultimate": "虫之呼吸·蜈蚣之舞", "wish_text": "「鬼，真是可恨呢♪」"},
    "muichiro": {"name": "时透无一郎", "anime": "鬼灭之刃", "element": "鬼杀队·霞柱", "rarity": 4, "title": "霞柱", "desc": "十四岁成为柱的天才，总是看着云发呆。", "ability": "霞之呼吸", "ultimate": "霞之呼吸·壹之型·垂天远霞", "wish_text": "「……你是谁来着？」"},
    "loid": {"name": "劳埃德·福杰", "anime": "间谍过家家", "element": "WISE", "rarity": 4, "title": "黄昏", "desc": "为世界和平组建临时家庭的顶级间谍。", "ability": "间谍技能全开", "ultimate": "作战代号·枭", "wish_text": "「为了世界的和平，行动代号：枭。」"},
    "yor": {"name": "约尔·福杰", "anime": "间谍过家家", "element": "花园", "rarity": 4, "title": "荆棘公主", "desc": "白天是职员，晚上是杀人无数的荆棘公主。", "ability": "超人身体能力", "ultimate": "荆棘公主·一闪", "wish_text": "「我是荆棘公主。」"},
    "hinata_shoyo": {"name": "日向翔阳", "anime": "排球少年", "element": "乌野高中", "rarity": 4, "title": "最强诱饵", "desc": "个子小但跳得高的排球笨蛋。", "ability": "超弹跳·快攻", "ultimate": "乌野快攻·怪人快攻", "wish_text": "「我还能跳得更高！」"},
    "kageyama": {"name": "影山飞雄", "anime": "排球少年", "element": "乌野高中", "rarity": 4, "title": "场上之王", "desc": "把球送到最好打的位置的王者二传。", "ability": "精准二传", "ultimate": "场上之王·变速托球", "wish_text": "「我会把球送到最好打的位置。」"},
    "takumi": {"name": "藤原拓海", "anime": "头文字D", "element": "秋名山", "rarity": 4, "title": "AE86之神", "desc": "送豆腐送出漂移神话的秋名山车神。", "ability": "惯性漂移", "ultimate": "排水渠过弯", "wish_text": "「排水渠过弯，看好了。」"},
}

# ============================================================
# 三星角色（27）
# ============================================================
THREE_STAR_CHARS = {
    "nami": {"name": "娜美", "anime": "海贼王", "element": "草帽一伙", "rarity": 3, "title": "小贼猫", "desc": "草帽团航海士，精通气象学，最爱钱和橘子。", "ability": "天候棒·气象学", "ultimate": "雷电天候", "wish_text": "「钱是最重要的！」"},
    "sakura": {"name": "春野樱", "anime": "火影忍者", "element": "木叶·第七班", "rarity": 3, "title": "怪力医疗忍者", "desc": "纲手的弟子，怪力与医疗忍术兼备。", "ability": "怪力·百豪之术", "ultimate": "樱花冲", "wish_text": "「我终于追上他们了！」"},
    "trunks": {"name": "特兰克斯", "anime": "龙珠", "element": "未来战士", "rarity": 3, "title": "未来少年", "desc": "来自绝望未来的赛亚人混血战士。", "ability": "超级赛亚人·剑术", "ultimate": "燃烧攻击", "wish_text": "「我来自未来，为了改变过去。」"},
    "orihime": {"name": "井上织姬", "anime": "死神", "element": "死神代理同行者", "rarity": 3, "title": "盾舜六花", "desc": "拥有拒绝之力的治愈系少女。", "ability": "盾舜六花", "ultimate": "三天结盾·拒绝", "wish_text": "「我要保护大家！」"},
    "inosuke": {"name": "嘴平伊之助", "anime": "鬼灭之刃", "element": "鬼杀队", "rarity": 3, "title": "兽之呼吸", "desc": "戴野猪头套的兽之剑士，猪突猛进！", "ability": "兽之呼吸·触觉", "ultimate": "獠牙撕扯", "wish_text": "「猪突猛进！猪突猛进！」"},
    "mikasa": {"name": "三笠·阿克曼", "anime": "进击的巨人", "element": "调查兵团", "rarity": 3, "title": "东洋人末裔", "desc": "战斗力仅次于利威尔的天才少女。", "ability": "阿克曼之力·立体机动", "ultimate": "二刀流斩击", "wish_text": "「只要有你在，我就无所不能。」"},
    "fushiguro": {"name": "伏黑惠", "anime": "咒术回战", "element": "东京咒术高专", "rarity": 3, "title": "十种影法术", "desc": "禅院家血脉的一级候补咒术师。", "ability": "十种影法术", "ultimate": "玉犬·鵺", "wish_text": "「我要让不平等的人，得到平等的救赎。」"},
    "kurapika": {"name": "酷拉皮卡", "anime": "全职猎人", "element": "猎人协会", "rarity": 3, "title": "窟卢塔族幸存者", "desc": "为族人复仇的火红眼持有者。", "ability": "具现化系·锁链", "ultimate": "律制小指之链", "wish_text": "「我要把同伴的眼睛，全部夺回来。」"},
    "kurama": {"name": "藏马", "anime": "幽游白书", "element": "灵界侦探组", "rarity": 3, "title": "妖狐", "desc": "化为人形的千年妖狐，植物系妖怪。", "ability": "植物操纵·妖狐形态", "ultimate": "风华圆舞阵", "wish_text": "「玫瑰的刺，是很痛的。」"},
    "usopp": {"name": "乌索普", "anime": "海贼王", "element": "草帽一伙", "rarity": 3, "title": "狙击王", "desc": "吹牛8000部下的狙击手，勇敢的海上战士。", "ability": "狙击·弹弓", "ultimate": "必杀·绿星·冲击狼草", "wish_text": "「我是乌索普船长！有8000部下！」"},
    "chopper": {"name": "托尼托尼·乔巴", "anime": "海贼王", "element": "草帽一伙", "rarity": 3, "title": "船医", "desc": "吃了人人果实的驯鹿，会七段变形的船医。", "ability": "人人果实·蓝波球", "ultimate": "怪物形态", "wish_text": "「我是狸猫……不对，是驯鹿！」"},
    "hinata": {"name": "日向雏田", "anime": "火影忍者", "element": "木叶·日向家", "rarity": 3, "title": "白眼的公主", "desc": "温柔却坚韧的日向家长女。", "ability": "白眼·柔拳", "ultimate": "八卦六十四掌", "wish_text": "「我也想变得坚强。」"},
    "miyagi": {"name": "宫城良田", "anime": "灌篮高手", "element": "湘北高中", "rarity": 3, "title": "湘北队长", "desc": "身高168的王牌控卫，速度就是武器。", "ability": "闪电运球·抢断", "ultimate": "超速突破", "wish_text": "「速度就是我的武器。」"},
    "ran": {"name": "毛利兰", "anime": "名侦探柯南", "element": "帝丹高中", "rarity": 3, "title": "空手道主将", "desc": "空手道部主将，等待新一归来的少女。", "ability": "空手道", "ultimate": "回旋踢", "wish_text": "「新一，你在哪里……」"},
    "hanji": {"name": "韩吉·佐耶", "anime": "进击的巨人", "element": "调查兵团", "rarity": 3, "title": "巨人狂热者", "desc": "对巨人爱到疯狂的科学家分队长。", "ability": "立体机动·科学脑", "ultimate": "巨人捕获装置", "wish_text": "「巨人真是太浪漫了！」"},
    "winry": {"name": "温莉·洛克贝尔", "anime": "钢之炼金术师", "element": "机械铠技师", "rarity": 3, "title": "机械铠技师", "desc": "为艾尔利克兄弟修理机械铠的天才技师。", "ability": "机械铠维修", "ultimate": "扳手暴击", "wish_text": "「机械铠要好好保养哦！」"},
    "nana": {"name": "娜娜莉·兰佩路基", "anime": "Code Geass", "element": "布里塔尼亚皇族", "rarity": 3, "title": "失明的公主", "desc": "失明且不能行走的公主，却看得最远。", "ability": "超凡的记忆与心灵", "ultimate": "娜娜莉之愿", "wish_text": "「我希望的世界，是没有争斗的世界。」"},
    "illya": {"name": "伊莉雅斯菲尔", "anime": "Fate/stay night", "element": "爱因兹贝伦家", "rarity": 3, "title": "Master", "desc": "人造的圣杯少女，Berserker的主人。", "ability": "圣杯·魔術回路", "ultimate": "Berserker支配", "wish_text": "「Berserker，上！」"},
    "misa": {"name": "弥海砂", "anime": "死亡笔记", "element": "第二基拉", "rarity": 3, "title": "人气偶像", "desc": "拥有死神之眼的第二基拉。", "ability": "死神之眼", "ultimate": "交换半生·死亡笔记", "wish_text": "「弥砂是基拉的忠实信徒♪」"},
    "wendy": {"name": "温蒂·玛贝尔", "anime": "妖精的尾巴", "element": "妖精尾巴公会", "rarity": 3, "title": "天空魔导士", "desc": "天空之龙的灭龙魔导士，辅助与治愈。", "ability": "天空之灭龙魔法", "ultimate": "天空龙的咆哮", "wish_text": "「天龙的咆哮！」"},
    "krillin": {"name": "克林", "anime": "龙珠", "element": "地球战士", "rarity": 3, "title": "地球人最强", "desc": "没有尾巴没有血统却一直战斗到最后的人类。", "ability": "气功波·气圆斩", "ultimate": "气圆斩", "wish_text": "「悟空，拜托了！」"},
    "shinnosuke": {"name": "野原新之助", "anime": "蜡笔小新", "element": "双叶幼稚园", "rarity": 3, "title": "五岁的捣蛋鬼", "desc": "屁股威力无穷的五岁问题儿童。", "ability": "光屁屁·大人的暗号", "ultimate": "动感光波", "wish_text": "「动感光波——哔哔哔！」"},
    "usagi": {"name": "月野兔", "anime": "美少女战士", "element": "月亮王国", "rarity": 3, "title": "水手月亮", "desc": "爱哭爱吃的少女，却是爱与正义的水手服战士。", "ability": "月亮权杖", "ultimate": "月光公主权杖", "wish_text": "「代表月亮消灭你！」"},
    "sakura_card": {"name": "木之本樱", "anime": "魔卡少女樱", "element": "库洛魔法使", "rarity": 3, "title": "库洛牌持有者", "desc": "收服库洛牌的元气魔法少女。", "ability": "封印之杖·魔法", "ultimate": "库洛牌·收服", "wish_text": "「库洛牌，收服！」"},
    "taichi": {"name": "八神太一", "anime": "数码宝贝", "element": "被选召的孩子", "rarity": 3, "title": "勇气的队长", "desc": "被选召孩子们的领袖，勇气之徽章持有者。", "ability": "勇气之徽章", "ultimate": "与暴龙兽心意合一", "wish_text": "「勇气之徽章！」"},
    "agumon": {"name": "亚古兽", "anime": "数码宝贝", "element": "数码兽", "rarity": 3, "title": "爬虫类型", "desc": "太一的搭档数码兽，进化没有极限。", "ability": "小型火焰·进化", "ultimate": "暴龙兽·超级火焰", "wish_text": "「亚古兽，进化——暴龙兽！」"},
    "kagome": {"name": "日暮戈薇", "anime": "犬夜叉", "element": "巫女转世", "rarity": 3, "title": "桔梗的转世", "desc": "穿越到战国的现代少女，破魔之箭的巫女。", "ability": "破魔之箭·四魂之玉感知", "ultimate": "破魔矢", "wish_text": "「犬夜叉，坐下！」"},
}

# ============================================================
# 技能自动生成（还原原作，与角色一一对应，无学习数值）
# ============================================================
FIVE_STAR_SKILLS = {}
for _cid, _c in FIVE_STAR_CHARS.items():
    FIVE_STAR_SKILLS[_cid + "_ult"] = {
        "name": _c["ultimate"], "char": _cid, "rarity": 5, "type": "奥义",
        "effect": _c["ability"], "desc": f"{_c['name']}的终极奥义——{_c['ultimate']}。",
    }
FOUR_STAR_SKILLS = {}
for _cid, _c in FOUR_STAR_CHARS.items():
    FOUR_STAR_SKILLS[_cid + "_skill"] = {
        "name": _c["ultimate"], "char": _cid, "rarity": 4, "type": "招式",
        "effect": _c["ability"], "desc": f"{_c['name']}的得意技——{_c['ultimate']}。",
    }
ALL_SKILLS = {**FIVE_STAR_SKILLS, **FOUR_STAR_SKILLS}

# ============================================================
# 三星碎片（抽卡三星掉落，10个可合成随机四星技能）
# ============================================================
THREE_STAR_ITEMS = [
    {"name": "橡胶手枪碎片", "anime": "海贼王", "element": "海贼王", "desc": "路飞的基础招式碎片。"},
    {"name": "影分身碎片", "anime": "火影忍者", "element": "火影忍者", "desc": "鸣人的招牌忍术碎片。"},
    {"name": "龟派气功碎片", "anime": "龙珠", "element": "龙珠", "desc": "悟空的经典招式碎片。"},
    {"name": "始解斩月碎片", "anime": "死神", "element": "死神", "desc": "一护的斩魄刀碎片。"},
    {"name": "水之呼吸碎片", "anime": "鬼灭之刃", "element": "鬼灭之刃", "desc": "义勇的呼吸法碎片。"},
    {"name": "立体机动碎片", "anime": "进击的巨人", "element": "进击的巨人", "desc": "调查兵团的装备碎片。"},
    {"name": "咒力基础碎片", "anime": "咒术回战", "element": "咒术回战", "desc": "咒术师的基础能量碎片。"},
    {"name": "炼成阵碎片", "anime": "钢之炼金术师", "element": "钢之炼金术师", "desc": "炼金术的基础法阵碎片。"},
    {"name": "追踪眼镜碎片", "anime": "名侦探柯南", "element": "名侦探柯南", "desc": "柯南的道具碎片。"},
    {"name": "洞爷湖碎片", "anime": "银魂", "element": "银魂", "desc": "银时的木刀碎片。"},
    {"name": "篮球碎片", "anime": "灌篮高手", "element": "灌篮高手", "desc": "湘北的篮球碎片。"},
    {"name": "经验书", "anime": "全科", "element": "全科", "desc": "前辈留下的学习笔记。"},
    {"name": "替身之箭碎片", "anime": "JOJO", "element": "JOJO", "desc": "觉醒替身的神秘之箭碎片。"},
    {"name": "个性因子碎片", "anime": "我的英雄学院", "element": "我的英雄学院", "desc": "个性能力的遗传因子碎片。"},
    {"name": "精灵球碎片", "anime": "宝可梦", "element": "宝可梦", "desc": "捕捉宝可梦的精灵球碎片。"},
    {"name": "千年积木碎片", "anime": "游戏王", "element": "游戏王", "desc": "封印法老王的千年积木碎片。"},
    {"name": "魔法书碎片", "anime": "葬送的芙莉莲", "element": "葬送的芙莉莲", "desc": "一级魔法使考试的魔导书碎片。"},
    {"name": "伊甸学园星碎片", "anime": "间谍过家家", "element": "间谍过家家", "desc": "伊甸学园的 TOKI 星碎片。"},
    {"name": "四魂之玉碎片", "anime": "犬夜叉", "element": "犬夜叉", "desc": "四魂之玉的碎片。"},
    {"name": "逆刃刀碎片", "anime": "浪客剑心", "element": "浪客剑心", "desc": "誓不再杀的逆刃刀碎片。"},
]

# ============================================================
# 羁绊礼装（集齐指定角色组合，全队 XP 加成）
# ============================================================
BOND_SET_BONUSES = [
    {"anime": "海贼王", "chars": ["luffy", "zoro", "sanji"], "name": "草帽三主力", "bonus": 0.05, "desc": "集齐路飞+索隆+山治，全队 XP +5%"},
    {"anime": "火影忍者", "chars": ["naruto", "sasuke", "sakura", "kakashi"], "name": "第七班", "bonus": 0.05, "desc": "集齐第七班四人，全队 XP +5%"},
    {"anime": "鬼灭之刃", "chars": ["tanjiro", "nezuko", "zenitsu", "inosuke", "giyu"], "name": "鬼杀队", "bonus": 0.05, "desc": "集齐鬼杀队五人组，全队 XP +5%"},
    {"anime": "新世纪福音战士", "chars": ["shinji", "ayanami", "asuka", "kaworu"], "name": "NERV适格者", "bonus": 0.05, "desc": "集齐EVA适格者，全队 XP +5%"},
    {"anime": "灌篮高手", "chars": ["sakuragi", "rukawa", "mitsui", "miyagi"], "name": "湘北五虎", "bonus": 0.05, "desc": "集齐湘北主力，全队 XP +5%"},
    {"anime": "死神", "chars": ["ichigo", "rukia", "byakuya", "zaraki"], "name": "护廷十三队", "bonus": 0.05, "desc": "集齐死神四人组，全队 XP +5%"},
    {"anime": "家庭教师", "chars": ["tsuna", "reborn", "gokudera", "mukuro"], "name": "彭格列家族", "bonus": 0.05, "desc": "集齐彭格列四人，全队 XP +5%"},
    {"anime": "Fate/stay night", "chars": ["shirou", "saber", "rin", "gilgamesh"], "name": "圣杯战争", "bonus": 0.05, "desc": "集齐圣杯战争参战者，全队 XP +5%"},
    {"anime": "咒术回战", "chars": ["gojo", "itadori", "sukuna", "fushiguro"], "name": "咒术师们", "bonus": 0.05, "desc": "集齐咒术回战四人，全队 XP +5%"},
    {"anime": "全职猎人", "chars": ["gon", "killua"], "name": "猎人搭档", "bonus": 0.04, "desc": "集齐小杰+奇犽，全队 XP +4%"},
    {"anime": "JOJO的奇妙冒险", "chars": ["jotaro", "joseph", "kakyoin"], "name": "星尘远征军", "bonus": 0.04, "desc": "集齐JOJO远征军，全队 XP +4%"},
    {"anime": "幽游白书", "chars": ["yusuke", "hiei", "kurama"], "name": "灵界侦探组", "bonus": 0.04, "desc": "集齐幽游三人组，全队 XP +4%"},
    {"anime": "死亡笔记", "chars": ["light", "l"], "name": "Kira vs L", "bonus": 0.04, "desc": "集齐夜神月+L，全队 XP +4%"},
    {"anime": "间谍过家家", "chars": ["loid", "yor", "anya"], "name": "福杰一家", "bonus": 0.04, "desc": "集齐福杰一家，全队 XP +4%"},
    {"anime": "链锯人", "chars": ["denji", "power"], "name": "公安搭档", "bonus": 0.04, "desc": "集齐电次+帕瓦，全队 XP +4%"},
    {"anime": "妖精的尾巴", "chars": ["natsu", "lucy", "erza", "gray"], "name": "妖尾最强小队", "bonus": 0.05, "desc": "集齐妖尾四人，全队 XP +5%"},
    {"anime": "排球少年", "chars": ["hinata_shoyo", "kageyama"], "name": "乌野快攻双人组", "bonus": 0.04, "desc": "集齐日向+影山，全队 XP +4%"},
    {"anime": "鬼灭之刃·柱", "chars": ["rengoku", "shinobu", "muichiro"], "name": "柱合会议", "bonus": 0.04, "desc": "集齐三位柱，全队 XP +4%"},
]

# ============================================================
# 周主题池 & 主题羁绊
# ============================================================
WEEKLY_THEMES = [
    {"id": "shonen", "name": "🔥 热血少年周", "chars": ["luffy", "naruto", "goku", "natsu", "tanjiro", "tsuna", "gon", "ace", "deku", "denji", "yusuke"], "desc": "热血、友情、胜利！本周少年漫角色概率UP！", "up_rate": 0.5},
    {"id": "battle", "name": "⚔️ 战斗狂潮周", "chars": ["goku", "vegeta", "gojo", "levi", "ichigo", "eren", "saitama", "jotaro", "dio", "sukuna", "zaraki", "frieza"], "desc": "最强战士们集结！本周战斗系角色概率UP！", "up_rate": 0.5},
    {"id": "mystery", "name": "🔍 推理悬疑周", "chars": ["conan", "haibara", "light", "lelouch", "edward", "kid", "heiji", "akai", "l", "near"], "desc": "真相只有一个！本周推理系角色概率UP！", "up_rate": 0.5},
    {"id": "mecha", "name": "🤖 机甲科幻周", "chars": ["shinji", "ayanami", "asuka", "genos", "kaworu"], "desc": "EVA与改造人！本周科幻角色概率UP！", "up_rate": 0.5},
    {"id": "sword", "name": "🗡️ 剑士之魂周", "chars": ["zoro", "ichigo", "rukia", "giyu", "kirito", "erza", "law", "rengoku", "muichiro", "saber", "byakuya", "kenshin", "inuyasha"], "desc": "剑与刀的浪漫！本周剑士角色概率UP！", "up_rate": 0.5},
    {"id": "healing", "name": "💚 治愈日常周", "chars": ["nezuko", "orihime", "sakura_fate", "gintoki", "asuna", "frieren", "anya", "doraemon", "winry", "wendy", "usagi", "sakura_card"], "desc": "温柔治愈的角色们！本周治愈系角色概率UP！", "up_rate": 0.5},
    {"id": "genius", "name": "🧠 天才集结周", "chars": ["gojo", "lelouch", "light", "conan", "haibara", "cc", "shirou", "l", "near", "reborn", "itachi", "yugi"], "desc": "智商爆表的天才们！本周天才角色概率UP！", "up_rate": 0.5},
    {"id": "sports", "name": "🏀 运动热血周", "chars": ["sakuragi", "rukawa", "mitsui", "sendoh", "miyagi", "ryoma", "hinata_shoyo", "kageyama", "takumi"], "desc": "运动与激情！本周运动系角色概率UP！", "up_rate": 0.5},
]

THEME_BONDS = [
    {"id": "shonen_bond", "theme": "shonen", "name": "🔥 热血少年羁绊", "chars": ["luffy", "naruto", "goku"], "bonus": 0.05, "desc": "集齐路飞+鸣人+悟空，全队 XP +5%"},
    {"id": "battle_bond", "theme": "battle", "name": "⚔️ 最强战士羁绊", "chars": ["goku", "gojo", "levi"], "bonus": 0.05, "desc": "集齐悟空+五条悟+利威尔，全队 XP +5%"},
    {"id": "mystery_bond", "theme": "mystery", "name": "🔍 推理天才羁绊", "chars": ["conan", "l", "light"], "bonus": 0.05, "desc": "集齐柯南+L+夜神月，全队 XP +5%"},
    {"id": "mecha_bond", "theme": "mecha", "name": "🤖 机甲之魂羁绊", "chars": ["shinji", "ayanami", "asuka"], "bonus": 0.05, "desc": "集齐真嗣+绫波丽+明日香，全队 XP +5%"},
    {"id": "sword_bond", "theme": "sword", "name": "🗡️ 剑士羁绊", "chars": ["zoro", "ichigo", "saber"], "bonus": 0.05, "desc": "集齐索隆+一护+Saber，全队 XP +5%"},
]

# ============================================================
# 主题皮肤（按动漫解锁）
# ============================================================
THEMES = {
    "default": {"name": "默认（深紫黑）", "unlock": "默认解锁", "BG": "#0b0b18", "CARD": "#16162a", "ACCENT": "#8b5cf6", "ACCENT_HOVER": "#a78bfa", "BLUE": "#22d3ee", "GOLD": "#fbbf24", "TEXT": "#f5f5fa", "SUBTEXT": "#9494b8", "BORDER": "#2d2d50", "INPUT_BG": "#0e0e1c", "STAR5_BG": "#2a1f0e", "STAR4_BG": "#1f0e2a", "STAR3_BG": "#0e1f2a"},
    "onepiece": {"name": "大海贼时代（蓝金）", "unlock": "获得任意海贼王角色", "BG": "#0a1628", "CARD": "#0f1f3a", "ACCENT": "#1e88e5", "ACCENT_HOVER": "#42a5f5", "BLUE": "#29b6f6", "GOLD": "#ffd54f", "TEXT": "#e3f2fd", "SUBTEXT": "#78909c", "BORDER": "#1a3a5c", "INPUT_BG": "#0a1a2e", "STAR5_BG": "#2a2008", "STAR4_BG": "#0a1a3a", "STAR3_BG": "#0a1525"},
    "naruto": {"name": "忍界（橙黑）", "unlock": "获得任意火影忍者角色", "BG": "#1a0e08", "CARD": "#2a1508", "ACCENT": "#ff6f00", "ACCENT_HOVER": "#ff8f00", "BLUE": "#ffab40", "GOLD": "#ffd54f", "TEXT": "#fff3e0", "SUBTEXT": "#a1887f", "BORDER": "#4a2810", "INPUT_BG": "#1a0e08", "STAR5_BG": "#3a2008", "STAR4_BG": "#2a1508", "STAR3_BG": "#1a0e08"},
    "demonslayer": {"name": "鬼杀队（绿黑）", "unlock": "获得任意鬼灭之刃角色", "BG": "#0a1a0e", "CARD": "#0f2a15", "ACCENT": "#2e7d32", "ACCENT_HOVER": "#43a047", "BLUE": "#66bb6a", "GOLD": "#ffd54f", "TEXT": "#e8f5e9", "SUBTEXT": "#81c784", "BORDER": "#1a4a20", "INPUT_BG": "#0a1a0e", "STAR5_BG": "#2a2008", "STAR4_BG": "#0f2a15", "STAR3_BG": "#0a1a0e"},
    "eva": {"name": "NERV（紫绿）", "unlock": "获得任意新世纪福音战士角色", "BG": "#120a1a", "CARD": "#1a0f2a", "ACCENT": "#7b1fa2", "ACCENT_HOVER": "#9c27b0", "BLUE": "#00e676", "GOLD": "#ffd54f", "TEXT": "#f3e5f5", "SUBTEXT": "#ce93d8", "BORDER": "#3a1a5c", "INPUT_BG": "#120a1a", "STAR5_BG": "#2a2008", "STAR4_BG": "#1a0f2a", "STAR3_BG": "#120a1a"},
    "sao": {"name": "艾恩葛朗特（蓝白）", "unlock": "获得任意刀剑神域角色", "BG": "#0a0e1a", "CARD": "#0f1525", "ACCENT": "#00bcd4", "ACCENT_HOVER": "#26c6da", "BLUE": "#4dd0e1", "GOLD": "#ffd54f", "TEXT": "#e0f7fa", "SUBTEXT": "#80deea", "BORDER": "#1a2a4a", "INPUT_BG": "#0a0e1a", "STAR5_BG": "#2a2008", "STAR4_BG": "#0f1525", "STAR3_BG": "#0a0e1a"},
}

# ============================================================
# UP池轮换（每周切换）
# ============================================================
UP_ROTATION = ["luffy", "jotaro", "naruto", "goku", "sukuna", "ichigo", "tanjiro", "eren",
               "gojo", "ace", "shanks", "itachi", "saber", "lelouch", "l", "rengoku",
               "conan", "kid", "reborn", "all_might", "makima", "kaneki", "frieren",
               "pikachu", "doraemon", "kenshin", "inuyasha", "yugi", "gilgamesh", "saitama"]

# ============================================================
# 角色小课堂词汇（保留双语例句；未收录角色回退通用词库）
# ============================================================
CHAR_VOCABULARY = {
    "luffy": [
        {"word": "adventure", "meaning": "n. 冒险", "example": "Life is an adventure, sail forward!（人生是一场冒险，扬帆前行！）"},
        {"word": "persevere", "meaning": "v. 坚持不懈", "example": "He persevered until he became the Pirate King.（他坚持到成为海贼王。）"},
        {"word": "freedom", "meaning": "n. 自由", "example": "I fight for freedom, just like Luffy.（我为自由而战，就像路飞。）"},
        {"word": "ambition", "meaning": "n. 雄心", "example": "His ambition is to find the One Piece.（他的抱负是找到大秘宝。）"},
    ],
    "naruto": [
        {"word": "never give up", "meaning": "phr. 永不放弃", "example": "I never give up, that's my nindo!（我绝不放弃，这就是我的忍道！）"},
        {"word": "determination", "meaning": "n. 决心", "example": "His determination moved even the Hokage.（他的决心连火影都感动了。）"},
        {"word": "believe", "meaning": "v. 相信", "example": "Believe in yourself, just like Naruto.（相信自己，就像鸣人。）"},
        {"word": "hardworking", "meaning": "adj. 勤奋的", "example": "A hardworking underdog can become Hokage.（勤奋的吊车尾也能成为火影。）"},
    ],
    "goku": [
        {"word": "limitless", "meaning": "adj. 无限的", "example": "Goku's potential is limitless.（悟空的潜力是无限的。）"},
        {"word": "surpass", "meaning": "v. 超越", "example": "I will surpass my limits every day.（我每天都要超越极限。）"},
        {"word": "strength", "meaning": "n. 力量", "example": "True strength comes from training.（真正的力量来自训练。）"},
        {"word": "relentless", "meaning": "adj. 不懈的", "example": "His relentless training made him the strongest.（不懈训练让他最强。）"},
    ],
    "conan": [
        {"word": "ubiquitous", "meaning": "adj. 无处不在的", "example": "Smartphones are ubiquitous in modern life.（智能手机在现代生活中无处不在。）"},
        {"word": "deduce", "meaning": "v. 推断", "example": "Conan deduced the truth from a single clue.（柯南从一条线索推断出真相。）"},
        {"word": "evidence", "meaning": "n. 证据", "example": "There's only one truth, and evidence proves it.（真相只有一个，证据证明它。）"},
        {"word": "meticulous", "meaning": "adj. 一丝不苟的", "example": "A detective must be meticulous.（侦探必须一丝不苟。）"},
    ],
    "gojo": [
        {"word": "invincible", "meaning": "adj. 无敌的", "example": "Gojo is invincible because he is the strongest.（五条悟无敌，因为他最强。）"},
        {"word": "infinity", "meaning": "n. 无限", "example": "His Limitless creates infinity between him and attacks.（无下限术式创造无限。）"},
        {"word": "confident", "meaning": "adj. 自信的", "example": "Be confident, because you are the strongest.（自信点，因为你最强。）"},
        {"word": "overwhelm", "meaning": "v. 压倒", "example": "His power overwhelms all curses.（他的力量压倒所有咒灵。）"},
    ],
    "tanjiro": [
        {"word": "compassion", "meaning": "n. 同情", "example": "Tanjiro shows compassion even to demons.（炭治郎即使对鬼也有同情。）"},
        {"word": "resilient", "meaning": "adj. 有韧性的", "example": "Be resilient like Tanjiro, never break.（像炭治郎一样有韧性。）"},
        {"word": "kindness", "meaning": "n. 善良", "example": "Kindness is his greatest strength.（善良是他最大的力量。）"},
        {"word": "persist", "meaning": "v. 坚持", "example": "He persisted despite losing his family.（尽管失去家人他依然坚持。）"},
    ],
    "saitama": [
        {"word": "ordinary", "meaning": "adj. 普通的", "example": "An ordinary guy can become the strongest hero.（普通人也能成为最强英雄。）"},
        {"word": "consistency", "meaning": "n. 一致性", "example": "100 push-ups every day — consistency is power.（每天100俯卧撑——坚持就是力量。）"},
        {"word": "boredom", "meaning": "n. 无聊", "example": "Saitama fights boredom as much as villains.（埼玉对抗无聊就像对抗反派。）"},
        {"word": "effortless", "meaning": "adj. 不费力的", "example": "His victory looked effortless, but it took years.（胜利看似轻松，却花了数年。）"},
    ],
    "lelouch": [
        {"word": "strategy", "meaning": "n. 策略", "example": "Lelouch's strategy conquered the world.（鲁路修的策略征服世界。）"},
        {"word": "sacrifice", "meaning": "n./v. 牺牲", "example": "He made the ultimate sacrifice for peace.（他为和平做出终极牺牲。）"},
        {"word": "command", "meaning": "n./v. 命令", "example": "His Geass commands absolute obedience.（Geass命令绝对服从。）"},
        {"word": "brilliant", "meaning": "adj. 杰出的", "example": "A brilliant mind can change the world.（杰出的头脑能改变世界。）"},
    ],
    "shinji": [
        {"word": "escape", "meaning": "v. 逃避", "example": "Don't escape from your problems.（不要逃避问题。）"},
        {"word": "courage", "meaning": "n. 勇气", "example": "It takes courage to face reality.（面对现实需要勇气。）"},
        {"word": "anxiety", "meaning": "n. 焦虑", "example": "Shinji's anxiety is relatable to students.（真嗣的焦虑让学生感同身受。）"},
        {"word": "accept", "meaning": "v. 接受", "example": "Learn to accept yourself.（学会接受自己。）"},
    ],
    "kirito": [
        {"word": "survive", "meaning": "v. 生存", "example": "He survived a death game with skill.（他靠技术在死亡游戏中生存。）"},
        {"word": "dual", "meaning": "adj. 双重的", "example": "His dual-wielding style is unique.（二刀流风格独一无二。）"},
        {"word": "virtual", "meaning": "adj. 虚拟的", "example": "In a virtual world, real bonds matter.（虚拟世界中真实羁绊更重要。）"},
        {"word": "overcome", "meaning": "v. 克服", "example": "Overcome the boss, clear the game.（克服Boss，通关游戏。）"},
    ],
    "edward": [
        {"word": "equivalent", "meaning": "adj. 等价的", "example": "Equivalent exchange: to gain, you must give.（等价交换：要得到必须付出。）"},
        {"word": "principle", "meaning": "n. 原则", "example": "He lives by the principle of equivalent exchange.（他以等价交换为原则。）"},
        {"word": "transmute", "meaning": "v. 使变形", "example": "Alchemists transmute matter into weapons.（炼金术师将物质转化为武器。）"},
        {"word": "resolve", "meaning": "n. 决心", "example": "His resolve never wavered.（他的决心从未动摇。）"},
    ],
    "eren": [
        {"word": "freedom", "meaning": "n. 自由", "example": "Eren fights for freedom beyond the walls.（艾伦为墙外的自由而战。）"},
        {"word": "devote", "meaning": "v. 献身", "example": "He devoted his life to the survey corps.（他献身于调查兵团。）"},
        {"word": "barrier", "meaning": "n. 障碍", "example": "Break through every barrier.（突破每一个障碍。）"},
        {"word": "rage", "meaning": "n. 愤怒", "example": "His rage fuels his Titan power.（愤怒激发他的巨人之力。）"},
    ],
    "ichigo": [
        {"word": "protect", "meaning": "v. 保护", "example": "I will protect everything I can.（我要保护一切。）"},
        {"word": "instinct", "meaning": "n. 本能", "example": "His Hollow instincts make him stronger.（虚的本能让他更强。）"},
        {"word": "slash", "meaning": "v. 砍", "example": "One slash of Zangetsu ends the fight.（斩月一击结束战斗。）"},
        {"word": "resolve", "meaning": "n. 决心", "example": "His resolve to protect is unbreakable.（保护的决心坚不可摧。）"},
    ],
    "gon": [
        {"word": "potential", "meaning": "n. 潜力", "example": "Gon's potential as an Enhancer is enormous.（小杰强化系的潜力巨大。）"},
        {"word": "curious", "meaning": "adj. 好奇的", "example": "Be curious about the world, like Gon.（像小杰一样对世界好奇。）"},
        {"word": "hunt", "meaning": "v. 狩猎", "example": "Hunt for knowledge every day.（每天猎取知识。）"},
        {"word": "grow", "meaning": "v. 成长", "example": "Every challenge makes you grow.（每个挑战让你成长。）"},
    ],
    "gintoki": [
        {"word": "lazy", "meaning": "adj. 懒惰的", "example": "Gintoki is lazy but reliable when it matters.（银时懒但关键时刻可靠。）"},
        {"word": "sugar", "meaning": "n. 糖", "example": "Strawberry milk gives sugar for studying.（草莓牛奶给学习补糖。）"},
        {"word": "samurai", "meaning": "n. 武士", "example": "A samurai's soul doesn't break.（武士之魂不会折断。）"},
        {"word": "relax", "meaning": "v. 放松", "example": "Sometimes you need to relax before studying.（有时学习前需要放松。）"},
    ],
    "sakuragi": [
        {"word": "genius", "meaning": "n. 天才", "example": "I am a genius!（我是天才！）"},
        {"word": "rebound", "meaning": "n. 篮板", "example": "Grab every rebound in life.（抓住人生的每个篮板。）"},
        {"word": "passionate", "meaning": "adj. 热情的", "example": "His passionate spirit inspires teammates.（热情激励队友。）"},
        {"word": "rookie", "meaning": "n. 新手", "example": "Even a rookie can become the ace.（新人也能成为王牌。）"},
    ],
    "natsu": [
        {"word": "flame", "meaning": "n. 火焰", "example": "Let your passion burn like a flame.（让热情如火焰燃烧。）"},
        {"word": "guild", "meaning": "n. 公会", "example": "Fairy Tail is more than a guild, it's family.（妖尾不只是公会，更是家人。）"},
        {"word": "roar", "meaning": "v. 咆哮", "example": "Roar your determination out loud!（大声吼出决心！）"},
        {"word": "comrade", "meaning": "n. 伙伴", "example": "Fight for your comrades.（为伙伴而战。）"},
    ],
    "tsuna": [
        {"word": "worthless", "meaning": "adj. 没用的", "example": "From worthless loser to boss, anything is possible.（从废柴到首领，一切皆可能。）"},
        {"word": "family", "meaning": "n. 家族", "example": "I will protect my family.（我要保护家族。）"},
        {"word": "hyper", "meaning": "adj. 超级的", "example": "Enter Hyper Dying Will Mode!（进入超死气模式！）"},
        {"word": "tutor", "meaning": "n. 家庭教师", "example": "A good tutor changes your life.（好家庭教师改变人生。）"},
    ],
    "shirou": [
        {"word": "ideal", "meaning": "n. 理想", "example": "His ideal is to be an ally of justice.（他的理想是正义的伙伴。）"},
        {"word": "projection", "meaning": "n. 投影", "example": "Projection magic creates swords from nothing.（投影魔术从无中造剑。）"},
        {"word": "forge", "meaning": "v. 锻造", "example": "Forge your own path in life.（锻造自己的人生道路。）"},
        {"word": "sacrifice", "meaning": "n. 牺牲", "example": "An ideal requires sacrifice.（理想需要牺牲。）"},
    ],
    "asuka": [
        {"word": "pride", "meaning": "n. 骄傲", "example": "Her pride drives her to be the best.（骄傲驱使她成为最好。）"},
        {"word": "talent", "meaning": "n. 天赋", "example": "Talent plus hard work equals success.（天赋加努力等于成功。）"},
        {"word": "compete", "meaning": "v. 竞争", "example": "Compete with yourself, not others.（和自己竞争，而非别人。）"},
        {"word": "idiot", "meaning": "n. 笨蛋", "example": "Don't be an idiot — study harder!（别当笨蛋——更努力地学习！）"},
    ],
    "ayanami": [
        {"word": "silence", "meaning": "n. 沉默", "example": "Silence helps concentration.（沉默有助于专注。）"},
        {"word": "identity", "meaning": "n. 身份", "example": "Finding your identity is part of growing up.（找到自我是成长的一部分。）"},
        {"word": "pale", "meaning": "adj. 苍白的", "example": "Her pale blue hair matches the sky.（淡蓝的头发和天空相配。）"},
        {"word": "exist", "meaning": "v. 存在", "example": "Why do I exist? To grow, of course.（我为何存在？当然是为了成长。）"},
    ],
    "asuna": [
        {"word": "swift", "meaning": "adj. 迅速的", "example": "Be swift in answering questions.（回答问题要迅速。）"},
        {"word": "graceful", "meaning": "adj. 优雅的", "example": "Her rapier style is graceful and deadly.（细剑风格优雅而致命。）"},
        {"word": "companion", "meaning": "n. 同伴", "example": "A good companion makes the journey easier.（好同伴让旅程更轻松。）"},
        {"word": "raid", "meaning": "n. 攻坚", "example": "Raid the challenge with preparation.（带着准备去攻坚。）"},
    ],
    "genos": [
        {"word": "cyborg", "meaning": "n. 半机械人", "example": "Genos is a cyborg disciple of Saitama.（杰诺斯是埼玉的改造人弟子。）"},
        {"word": "analyze", "meaning": "v. 分析", "example": "Analyze your mistakes carefully.（仔细分析错误。）"},
        {"word": "upgrade", "meaning": "v. 升级", "example": "Upgrade your knowledge every day.（每天升级知识。）"},
        {"word": "disciple", "meaning": "n. 弟子", "example": "Be a humble disciple of knowledge.（做知识的谦卑弟子。）"},
    ],
    "cc": [
        {"word": "contract", "meaning": "n. 契约", "example": "A contract binds us to our goals.（契约将我们与目标绑定。）"},
        {"word": "immortal", "meaning": "adj. 不朽的", "example": "Knowledge makes you immortal.（知识让你不朽。）"},
        {"word": "mysterious", "meaning": "adj. 神秘的", "example": "The witch kept her past mysterious.（魔女对自己的过去保持神秘。）"},
        {"word": "rebel", "meaning": "v./n. 反抗", "example": "Zero led the rebellion against the empire.（ZERO领导了对抗帝国的反抗。）"},
    ],
    "haibara": [
        {"word": "scientist", "meaning": "n. 科学家", "example": "Think like a scientist when solving problems.（解题时像科学家思考。）"},
        {"word": "formula", "meaning": "n. 公式", "example": "Memorize the formula for success.（记住成功的公式。）"},
        {"word": "cautious", "meaning": "adj. 谨慎的", "example": "Be cautious with tricky questions.（对狡猾的问题要谨慎。）"},
        {"word": "compound", "meaning": "n. 化合物", "example": "APTX4869 is a mysterious compound.（APTX4869是神秘的化合物。）"},
    ],
    "light": [
        {"word": "justice", "meaning": "n. 正义", "example": "Kira believes he is justice.（基拉相信自己就是正义。）"},
        {"word": "notebook", "meaning": "n. 笔记本", "example": "Write new words in your notebook.（把新单词写在笔记本上。）"},
        {"word": "eliminate", "meaning": "v. 消除", "example": "Eliminate wrong answers first.（先排除错误答案。）"},
        {"word": "manipulate", "meaning": "v. 操控", "example": "He tried to manipulate everyone around him.（他试图操控身边的所有人。）"},
    ],
    "zoro": [
        {"word": "direction", "meaning": "n. 方向", "example": "Zoro has no sense of direction, but you should.（索隆没方向感，但你该有。）"},
        {"word": "sword", "meaning": "n. 剑", "example": "Three swords, one goal — be the best.（三把刀，一个目标——做到最好。）"},
        {"word": "training", "meaning": "n. 训练", "example": "Daily training makes a swordsman.（每日训练成就剑士。）"},
        {"word": "loyal", "meaning": "adj. 忠诚的", "example": "A loyal crewmate never abandons the captain.（忠诚的船员从不抛弃船长。）"},
    ],
    "sanji": [
        {"word": "cuisine", "meaning": "n. 烹饪", "example": "Good cuisine needs good ingredients.（好烹饪需要好食材。）"},
        {"word": "gentleman", "meaning": "n. 绅士", "example": "Be a gentleman under pressure.（在压力下也要做绅士。）"},
        {"word": "flavor", "meaning": "n. 风味", "example": "Add flavor to your life with hobbies.（用爱好给生活加味。）"},
        {"word": "serve", "meaning": "v. 服务", "example": "He serves the best dishes to ladies first.（他把最好的菜先端给女士。）"},
    ],
    "sasuke": [
        {"word": "revenge", "meaning": "n. 复仇", "example": "Don't let revenge consume your life.（别让复仇吞噬你的人生。）"},
        {"word": "solitary", "meaning": "adj. 孤独的", "example": "Solitary study can be productive.（独自学习也可以高效。）"},
        {"word": "path", "meaning": "n. 道路", "example": "Choose your own path, like Sasuke.（像佐助一样选择自己的道路。）"},
        {"word": "shadow", "meaning": "n. 影子", "example": "He walked in the shadow of hatred for years.（他在仇恨的阴影下走了多年。）"},
    ],
    "kakashi": [
        {"word": "copy", "meaning": "v. 复制", "example": "Copy good writing styles.（模仿好的写作风格。）"},
        {"word": "punctual", "meaning": "adj. 守时的", "example": "Kakashi is always late — don't be like him for exams!（卡卡西总迟到——考试可别学他！）"},
        {"word": "versatile", "meaning": "adj. 多才多艺的", "example": "A versatile ninja knows a thousand jutsu.（多才多艺的忍者会千种忍术。）"},
        {"word": "teamwork", "meaning": "n. 团队合作", "example": "Those who abandon their teammates are worse than trash.（抛弃同伴的人比垃圾还不如。）"},
    ],
    "levi": [
        {"word": "clean", "meaning": "adj. 干净的", "example": "Keep your study desk clean.（保持书桌整洁。）"},
        {"word": "precise", "meaning": "adj. 精确的", "example": "Be precise in your answers.（答案要精确。）"},
        {"word": "discipline", "meaning": "n. 纪律", "example": "Discipline is his weapon.（纪律是他的武器。）"},
        {"word": "abandon", "meaning": "v. 放弃", "example": "Never abandon your dreams.（永不放弃梦想。）"},
    ],
    "itadori": [
        {"word": "athletic", "meaning": "adj. 运动的", "example": "An athletic body supports an athletic mind.（健壮的身体支撑敏捷的头脑。）"},
        {"word": "curse", "meaning": "n. 诅咒", "example": "Don't curse difficult exams, conquer them.（别诅咒难题，去征服它们。）"},
        {"word": "swallow", "meaning": "v. 吞下", "example": "Swallow your fear and move on.（吞下恐惧，继续前进。）"},
        {"word": "descend", "meaning": "v. 降临", "example": "The King of Curses descended into his body.（诅咒之王降临到他体内。）"},
    ],
    "killua": [
        {"word": "lightning", "meaning": "n. 闪电", "example": "Killua's lightning-fast reflexes.（奇犽闪电般的反应。）"},
        {"word": "assassin", "meaning": "n. 刺客", "example": "Be an assassin of bad habits.（做坏习惯的刺客。）"},
        {"word": "friendship", "meaning": "n. 友谊", "example": "Friendship makes you stronger.（友谊让你更强。）"},
        {"word": "speed", "meaning": "n. 速度", "example": "Increase your reading speed.（提高阅读速度。）"},
    ],
    "nezuko": [
        {"word": "gentle", "meaning": "adj. 温柔的", "example": "Nezuko is gentle even as a demon.（祢豆子即使是鬼也温柔。）"},
        {"word": "family", "meaning": "n. 家人", "example": "Study for your family's pride.（为家人的骄傲而学习。）"},
        {"word": "silent", "meaning": "adj. 沉默的", "example": "Silent study mode: activated.（静音学习模式：启动。）"},
        {"word": "resist", "meaning": "v. 抵抗", "example": "She resists the demon's hunger.（她抵抗着鬼的饥饿。）"},
    ],
    "zenitsu": [
        {"word": "fear", "meaning": "n. 恐惧", "example": "Zenitsu fears everything but fights anyway.（善逸什么都怕，但依然战斗。）"},
        {"word": "sleep", "meaning": "n./v. 睡觉", "example": "Sleep consolidates memory, get enough rest.（睡眠巩固记忆，保证休息。）"},
        {"word": "thunder", "meaning": "n. 雷", "example": "Thunder Breathing: first form!（雷之呼吸：壹之型！）"},
        {"word": "flash", "meaning": "n. 闪光", "example": "A flash of lightning ended the battle.（一道闪电结束了战斗。）"},
    ],
    "mikasa": [
        {"word": "devotion", "meaning": "n. 献身", "example": "Mikasa's devotion to Eren is absolute.（三笠对艾伦的献身是绝对的。）"},
        {"word": "scarf", "meaning": "n. 围巾", "example": "A warm scarf for cold study nights.（寒冷学习夜的温暖围巾。）"},
        {"word": "unstoppable", "meaning": "adj. 不可阻挡的", "example": "Be unstoppable in your prep.（备考路上不可阻挡。）"},
        {"word": "beloved", "meaning": "adj. 心爱的", "example": "Study for your beloved dreams.（为心爱的梦想而学习。）"},
    ],
    "vegeta": [
        {"word": "prince", "meaning": "n. 王子", "example": "The Saiyan prince never bows.（赛亚人王子从不低头。）"},
        {"word": "pride", "meaning": "n. 自尊", "example": "Take pride in your progress.（为进步感到自豪。）"},
        {"word": "rival", "meaning": "n. 对手", "example": "A good rival pushes you to improve.（好对手促使你进步。）"},
        {"word": "ultimately", "meaning": "adv. 最终", "example": "He ultimately surpassed his limits.（他最终超越了极限。）"},
    ],
    "rukia": [
        {"word": "noble", "meaning": "adj. 高贵的", "example": "Noble birth doesn't define you, effort does.（高贵出身不定义你，努力才是。）"},
        {"word": "elegant", "meaning": "adj. 优雅的", "example": "Write elegant sentences in your essay.（作文中写出优雅句子。）"},
        {"word": "frost", "meaning": "n. 霜", "example": "Her zanpakuto controls frost and ice.（她的斩魄刀操控霜与冰。）"},
        {"word": "rely", "meaning": "v. 依靠", "example": "Rely on your teammates when needed.（需要时依靠队友。）"},
    ],
    "rukawa": [
        {"word": "ace", "meaning": "n. 王牌", "example": "Be the ace of your team.（做团队的王牌。）"},
        {"word": "shoot", "meaning": "v. 投篮", "example": "Shoot for your goals.（为你的目标出手。）"},
        {"word": "cool", "meaning": "adj. 冷静的", "example": "Stay cool under pressure.（压力下保持冷静。）"},
        {"word": "score", "meaning": "v./n. 得分", "example": "He scores every time.（他每次都得分。）"},
    ],
    "law": [
        {"word": "surgery", "meaning": "n. 外科手术", "example": "Law's ROOM allows precise surgery.（罗的ROOM允许精确手术。）"},
        {"word": "space", "meaning": "n. 空间", "example": "Create a focused study space.（创造专注学习的空间。）"},
        {"word": "tactical", "meaning": "adj. 战术的", "example": "Use tactical thinking in exams.（考试中使用战术思维。）"},
        {"word": "surgeon", "meaning": "n. 外科医生", "example": "The surgeon of death strikes precisely.（死亡外科医生精准出手。）"},
    ],
    "alphonse": [
        {"word": "soul", "meaning": "n. 灵魂", "example": "Alphonse's soul is bound to armor.（阿尔冯斯的灵魂绑定在铠甲上。）"},
        {"word": "armor", "meaning": "n. 铠甲", "example": "Put on your armor of knowledge.（穿上知识的铠甲。）"},
        {"word": "brother", "meaning": "n. 兄弟", "example": "Study with a brother for motivation.（和兄弟一起学习更有动力。）"},
        {"word": "restore", "meaning": "v. 恢复", "example": "They hope to restore their bodies.（他们希望恢复自己的身体。）"},
    ],
    "orihime": [
        {"word": "heal", "meaning": "v. 治愈", "example": "Orihime can reject and heal anything.（织姬能拒绝和治愈一切。）"},
        {"word": "reject", "meaning": "v. 拒绝", "example": "Reject wrong answers in multiple choice.（选择题中拒绝错误答案。）"},
        {"word": "shield", "meaning": "n. 盾牌", "example": "Shield your focus from distractions.（保护专注不受干扰。）"},
        {"word": "kind", "meaning": "adj. 善良的", "example": "Be kind to yourself when you fail.（失败时对自己善良一点。）"},
    ],
    "inosuke": [
        {"word": "beast", "meaning": "n. 野兽", "example": "Beast Breathing: wild and powerful.（兽之呼吸：狂野而强大。）"},
        {"word": "charge", "meaning": "v. 冲锋", "example": "Charge into your study session!（冲进学习时间！）"},
        {"word": "instinct", "meaning": "n. 直觉", "example": "His beast instinct finds hidden doors.（他的野兽直觉能找到隐藏的门。）"},
        {"word": "wild", "meaning": "adj. 狂野的", "example": "Wild enthusiasm for learning!（对学习的狂野热情！）"},
    ],
    "fushiguro": [
        {"word": "shikigami", "meaning": "n. 式神", "example": "Summon your shikigami of knowledge.（召唤知识式神。）"},
        {"word": "divine", "meaning": "adj. 神圣的", "example": "The Ten Shadows Technique is divine.（十种影法术是神圣的。）"},
        {"word": "salvation", "meaning": "n. 救赎", "example": "Success is your salvation from worry.（成功是把你从焦虑中救赎的方式。）"},
        {"word": "equal", "meaning": "adj. 平等的", "example": "He wants equal salvation for all.（他想让所有人得到平等救赎。）"},
    ],
    "kurapika": [
        {"word": "chain", "meaning": "n. 锁链", "example": "Kurapika's chains bind enemies.（酷拉皮卡的锁链束缚敌人。）"},
        {"word": "memory", "meaning": "n. 记忆", "example": "Train your memory every day.（每天训练记忆。）"},
        {"word": "scarlet", "meaning": "adj. 猩红的", "example": "Scarlet eyes of determination.（决心的火红眼。）"},
        {"word": " vow ", "meaning": "n. 誓约", "example": "A vow gives his chains power.（誓约赋予锁链力量。）"},
    ],
    # ---- 新增角色词汇 ----
    "jotaro": [
        {"word": "composure", "meaning": "n. 镇静", "example": "Jotaro keeps his composure in any crisis.（承太郎在任何危机中都保持镇静。）"},
        {"word": "precision", "meaning": "n. 精密", "example": "Star Platinum strikes with precision.（白金之星精准出击。）"},
        {"word": "intimidate", "meaning": "v. 威慑", "example": "His glare alone can intimidate enemies.（仅一个眼神就能威慑敌人。）"},
        {"word": "resolve", "meaning": "n. 决意", "example": "His resolve never wavers.（他的决意从不动摇。）"},
    ],
    "ace": [
        {"word": "flame", "meaning": "n. 火焰", "example": "The Flame Fist burns brighter than the sun.（火拳比太阳燃烧得更亮。）"},
        {"word": "brotherhood", "meaning": "n. 兄弟情", "example": "Their brotherhood never faded.（他们的兄弟情从未褪色。）"},
        {"word": "gratitude", "meaning": "n. 感激", "example": "His last word was gratitude.（他的遗言是感谢。）"},
        {"word": "inherit", "meaning": "v. 继承", "example": "Sabo inherited his flame.（萨博继承了他的火焰。）"},
    ],
    "rengoku": [
        {"word": "duty", "meaning": "n. 职责", "example": "He fulfilled his duty to the very end.（他到最后都履行了职责。）"},
        {"word": "blaze", "meaning": "v./n. 燃烧", "example": "Set your heart ablaze!（燃烧你的心吧！）"},
        {"word": "unyielding", "meaning": "adj. 不屈的", "example": "His unyielding spirit inspired everyone.（他不屈的精神激励了所有人。）"},
        {"word": "honor", "meaning": "n. 荣誉", "example": "He died with honor as a flame pillar.（他以炎柱之誉而死。）"},
    ],
    "saber": [
        {"word": "sovereign", "meaning": "n. 君主", "example": "The sovereign protects her kingdom.（君主守护她的王国。）"},
        {"word": "chivalry", "meaning": "n. 骑士精神", "example": "Chivalry guides her sword.（骑士精神指引她的剑。）"},
        {"word": "vow", "meaning": "n. 誓言", "example": "She kept her vow until the end.（她守誓言直到最后。）"},
        {"word": "blade", "meaning": "n. 剑刃", "example": "The sacred blade shines golden.（圣剑闪耀金光。）"},
    ],
    "l": [
        {"word": "deduction", "meaning": "n. 推理", "example": "His deduction cornered Kira.（他的推理逼入了基拉。）"},
        {"word": "probability", "meaning": "n. 概率", "example": "He calculates every probability.（他计算每一种概率。）"},
        {"word": "hunch", "meaning": "n. 直觉", "example": "His hunch was right about Kira.（他对基拉的直觉是对的。）"},
        {"word": "suspicion", "meaning": "n. 怀疑", "example": "Suspicion fell on the top student.（怀疑落在了优等生身上。）"},
    ],
    "reborn": [
        {"word": "mentor", "meaning": "n. 导师", "example": "A strict mentor builds a strong heir.（严格的导师造就强大的继承者。）"},
        {"word": "discipline", "meaning": "n. 训练", "example": "Discipline before talent.（先谈训练，再谈天赋。）"},
        {"word": "transformation", "meaning": "n. 蜕变", "example": "Tsuna's transformation began with Reborn.（阿纲的蜕变始于里包恩。）"},
        {"word": "legacy", "meaning": "n. 传承", "example": "He carries the Vongola legacy.（他背负着彭格列的传承。）"},
    ],
    "pikachu": [
        {"word": "electric", "meaning": "adj. 电的", "example": "Electric attacks charge with anger.（电系攻击随怒气而充能。）"},
        {"word": "companion", "meaning": "n. 搭档", "example": "A true companion never leaves your side.（真正的搭档从不离开你身边。）"},
        {"word": "loyal", "meaning": "adj. 忠诚的", "example": "Pikachu is loyal to Ash forever.（皮卡丘永远忠于小智。）"},
        {"word": "thunderbolt", "meaning": "n. 落雷", "example": "One thunderbolt won the gym battle.（一道落雷赢下了道馆战。）"},
    ],
    "doraemon": [
        {"word": "gadget", "meaning": "n. 小工具", "example": "A useful gadget solves many problems.（好用的工具解决很多问题。）"},
        {"word": "convenient", "meaning": "adj. 便利的", "example": "The Anywhere Door is so convenient.（任意门太方便了。）"},
        {"word": "future", "meaning": "n. 未来", "example": "Tools from the future change the past.（来自未来的工具改变过去。）"},
        {"word": "friendship", "meaning": "n. 友情", "example": "His friendship with Nobita is priceless.（和大雄的友情无价。）"},
    ],
    "frieren": [
        {"word": "eternal", "meaning": "adj. 永恒的", "example": "An eternal life needs eternal patience.（永恒的生命需要永恒的耐心。）"},
        {"word": "nostalgia", "meaning": "n. 怀旧", "example": "She collects spells out of nostalgia.（她因怀旧而收集魔法。）"},
        {"word": "incantation", "meaning": "n. 咒语", "example": "The incantation defeats demons.（这段咒语能消灭魔族。）"},
        {"word": "lifetime", "meaning": "n. 一生", "example": "A human lifetime is short to an elf.（人的一生对精灵来说很短暂。）"},
    ],
    "anya": [
        {"word": "telepathy", "meaning": "n. 读心", "example": "Her telepathy reveals everyone's secrets.（她的读心术看穿所有人的秘密。）"},
        {"word": "innocent", "meaning": "adj. 天真的", "example": "Her innocent smile heals the family.（她天真的笑容治愈了一家人。）"},
        {"word": "adopt", "meaning": "v. 收养", "example": "Loid adopted her for the mission.（劳埃德为了任务收养了她。）"},
        {"word": "harmony", "meaning": "n. 和平", "example": "She wishes for world harmony.（她祈愿世界和平。）"},
    ],
    "makima": [
        {"word": "dominate", "meaning": "v. 支配", "example": "She can dominate any living being.（她能支配任何生灵。）"},
        {"word": "contract", "meaning": "n. 契约", "example": "The devil's contract has a price.（恶魔的契约有代价。）"},
        {"word": "obedience", "meaning": "n. 服从", "example": "Absolute obedience is her power.（绝对服从是她的力量。）"},
        {"word": "leash", "meaning": "n. 项圈", "example": "Everyone is on her invisible leash.（所有人都拴在她无形的项圈上。）"},
    ],
    "kaneki": [
        {"word": "identity", "meaning": "n. 身份", "example": "He lost his identity overnight.（他一夜之间失去了身份。）"},
        {"word": "tragedy", "meaning": "n. 悲剧", "example": "A tragedy turned him into a ghoul.（一场悲剧让他变成喰种。）"},
        {"word": "endure", "meaning": "v. 忍受", "example": "He endures pain beyond imagination.（他忍受着超乎想象的痛苦。）"},
        {"word": "fragment", "meaning": "n. 碎片", "example": "1000 minus 7 — counting down the fragments.（1000减7——倒数着碎片。）"},
    ],
    "itachi": [
        {"word": "illusion", "meaning": "n. 幻术", "example": "His genjutsu creates perfect illusions.（他的幻术制造完美幻象。）"},
        {"word": "burden", "meaning": "n. 重担", "example": "He bore the burden alone.（他独自背负重担。）"},
        {"word": "clan", "meaning": "n. 家族", "example": "He chose the village over the clan.（他在家族与村子间选择了村子。）"},
        {"word": "sacrifice", "meaning": "n. 牺牲", "example": "His sacrifice saved his brother.（他的牺牲救了弟弟。）"},
    ],
    "inuyasha": [
        {"word": "stubborn", "meaning": "adj. 顽固的", "example": "The stubborn half-demon never admits defeat.（顽固的半妖从不认输。）"},
        {"word": "scent", "meaning": "n. 气味", "example": "He tracks enemies by scent.（他靠气味追踪敌人。）"},
        {"word": "blade", "meaning": "n. 刀刃", "example": "Tessaiga absorbs demonic power.（铁碎牙吸收妖力。）"},
        {"word": "reunion", "meaning": "n. 重逢", "example": "Every reunion begins a new journey.（每次重逢都是新旅程的开始。）"},
    ],
    "kenshin": [
        {"word": "wanderer", "meaning": "n. 浪人", "example": "The wanderer protects without a sword.（浪人不用剑也能守护。）"},
        {"word": "atonement", "meaning": "n. 赎罪", "example": "His sword fights for atonement.（他的剑为赎罪而挥。）"},
        {"word": "swift", "meaning": "adj. 迅捷的", "example": "His swift style ends fights in one strike.（他迅捷的剑术一击结束战斗。）"},
        {"word": "vow", "meaning": "n. 誓言", "example": "His vow: never to kill again.（他的誓言：不再杀人。）"},
    ],
    "yugi": [
        {"word": "duel", "meaning": "n. 决斗", "example": "The duel decides more than cards.（决斗决定的比卡牌更多。）"},
        {"word": "destiny", "meaning": "n. 命运", "example": "Their destiny is tied to the puzzle.（他们的命运与千年积木相连。）"},
        {"word": "trust", "meaning": "n. 信任", "example": "Trust your deck until the end.（相信你的卡组直到最后。）"},
        {"word": "courage", "meaning": "n. 勇气", "example": "Drawing the right card takes courage.（抽到正确的卡需要勇气。）"},
    ],
    "all_might": [
        {"word": "symbol", "meaning": "n. 象征", "example": "He was the symbol of peace.（他是和平的象征。）"},
        {"word": "heroism", "meaning": "n. 英雄气概", "example": "True heroism is saving with a smile.（真正的英雄气概是带着微笑去拯救。）"},
        {"word": "legacy", "meaning": "n. 遗产", "example": "He passed his legacy to the boy.（他把传承交给了少年。）"},
        {"word": "smile", "meaning": "n. 微笑", "example": "A hero's smile hides the pain.（英雄的微笑藏起痛苦。）"},
    ],
    "deku": [
        {"word": "persevere", "meaning": "v. 坚持", "example": "He persevered without a power for years.（他在没有力量的情况下坚持了多年。）"},
        {"word": "analysis", "meaning": "n. 分析", "example": "His hero analysis notebooks are legendary.（他的英雄分析笔记是传奇。）"},
        {"word": "inherit", "meaning": "v. 继承", "example": "He inherited One For All.（他继承了One For All。）"},
        {"word": "limit", "meaning": "n. 极限", "example": "Push beyond your limit carefully.（小心地突破极限。）"},
    ],
}

GENERAL_VOCABULARY = [
    {"word": "abundant", "meaning": "adj. 丰富的", "example": "Abundant practice leads to fluency.（充足练习带来流利。）"},
    {"word": "beneficial", "meaning": "adj. 有益的", "example": "Daily reading is beneficial for you.（每日阅读对你有益。）"},
    {"word": "comprehensive", "meaning": "adj. 全面的", "example": "A comprehensive review covers all topics.（全面复习覆盖所有话题。）"},
    {"word": "diligent", "meaning": "adj. 勤奋的", "example": "A diligent student never skips practice.（勤奋的学生从不跳过练习。）"},
    {"word": "enhance", "meaning": "v. 提高", "example": "Reading enhances your vocabulary.（阅读提高词汇量。）"},
    {"word": "fundamental", "meaning": "adj. 基本的", "example": "Grammar is fundamental to writing.（语法是写作基础。）"},
    {"word": "gradually", "meaning": "adv. 逐渐地", "example": "Your score improves gradually.（分数逐渐提高。）"},
    {"word": "hesitate", "meaning": "v. 犹豫", "example": "Don't hesitate to ask questions.（不要犹豫提问。）"},
    {"word": "inevitable", "meaning": "adj. 不可避免的", "example": "Mistakes are inevitable in learning.（学习中错误不可避免。）"},
    {"word": "justify", "meaning": "v. 证明正当", "example": "Justify your opinion with examples.（用例子证明观点。）"},
    {"word": "knowledgeable", "meaning": "adj. 知识渊博的", "example": "Be knowledgeable about current affairs.（对时事要渊博。）"},
    {"word": "lucrative", "meaning": "adj. 有利可图的", "example": "Hard skills open lucrative opportunities.（硬技能打开有利可图的机会。）"},
    {"word": "meticulous", "meaning": "adj. 一丝不苟的", "example": "Be meticulous in proofreading.（校对时一丝不苟。）"},
    {"word": "noteworthy", "meaning": "adj. 值得注意的", "example": "A noteworthy trend in the data.（数据中值得注意的趋势。）"},
    {"word": "obstacle", "meaning": "n. 障碍", "example": "Overcome every obstacle in your path.（克服路上每个障碍。）"},
    {"word": "persistent", "meaning": "adj. 坚持不懈的", "example": "Be persistent in daily study.（每日学习坚持不懈。）"},
    {"word": "qualify", "meaning": "v. 使合格", "example": "Hard work qualifies you for the chance.（努力使你有资格抓住机会。）"},
    {"word": "resilient", "meaning": "adj. 有韧性的", "example": "Be resilient when things go wrong.（出问题时要有韧性。）"},
    {"word": "significant", "meaning": "adj. 重要的", "example": "Practice makes a significant difference.（练习带来显著差异。）"},
    {"word": "tremendous", "meaning": "adj. 巨大的", "example": "You have made tremendous progress.（你取得了巨大进步。）"},
]


if __name__ == "__main__":
    print(f"角色总数：{len(FIVE_STAR_CHARS) + len(FOUR_STAR_CHARS) + len(THREE_STAR_CHARS)}"
          f"（五星 {len(FIVE_STAR_CHARS)} / 四星 {len(FOUR_STAR_CHARS)} / 三星 {len(THREE_STAR_CHARS)}）")
    print(f"技能总数：{len(ALL_SKILLS)}（自动从角色生成）")
