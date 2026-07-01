# 完整示例

这里展示几个从文字内容到最终视频的完整示例。

## 示例1：科技新闻视频

### 原始内容
```
苹果公司今天在加州总部举行秋季新品发布会，正式推出 iPhone 15 Pro 系列手机。
新机型搭载全新 A17 Pro 仿生芯片，采用3纳米工艺制程，性能提升35%。
iPhone 15 Pro 起售价999美元，将于9月22日正式开售。
```

### 拆分方案
```json
{
  "segments": [
    {
      "id": "apple-event",
      "category": "科技",
      "source": "Apple",
      "shots": [
        {
          "image": "media/apple-stage.jpg",
          "subtitle": "苹果公司今天举行秋季新品发布会",
          "durationSeconds": 4
        },
        {
          "image": "media/iphone15pro.jpg",
          "subtitle": "正式推出搭载 A17 Pro 芯片的 iPhone 15 Pro",
          "durationSeconds": 4
        },
        {
          "image": "media/a17-chip.jpg",
          "subtitle": "3纳米工艺，性能提升35%",
          "durationSeconds": 3
        },
        {
          "image": "media/price.jpg",
          "subtitle": "起售价999美元，9月22日开售",
          "durationSeconds": 3
        }
      ]
    }
  ]
}
```

### 图片搜索关键词
- 镜头1: `apple keynote stage` 或 `tech presentation`
- 镜头2: `iphone closeup` 或 `smartphone hand`
- 镜头3: `computer chip` 或 `processor technology`
- 镜头4: `price tag` 或 `shopping technology`

### 效果
- 总时长: 14秒
- 4个镜头
- 风格: 正式科技新闻

---

## 示例2：教程视频

### 原始内容
```
今天教大家做番茄炒蛋。
首先准备2个鸡蛋和2个番茄，鸡蛋打散备用。
番茄切块后，先炒蛋盛出，再炒番茄，最后混合翻炒加盐即可。
```

### 拆分方案
```json
{
  "segments": [
    {
      "id": "cooking-tutorial",
      "category": "美食教程",
      "source": "美食频道",
      "shots": [
        {
          "image": "media/ingredients.jpg",
          "subtitle": "准备2个鸡蛋和2个番茄",
          "durationSeconds": 3
        },
        {
          "image": "media/beat-eggs.jpg",
          "subtitle": "将鸡蛋打散备用",
          "durationSeconds": 3
        },
        {
          "image": "media/cut-tomato.jpg",
          "subtitle": "番茄切成小块",
          "durationSeconds": 3
        },
        {
          "image": "media/cook-eggs.jpg",
          "subtitle": "先将鸡蛋炒熟盛出",
          "durationSeconds": 4
        },
        {
          "image": "media/cook-tomato.jpg",
          "subtitle": "再炒番茄至软烂",
          "durationSeconds": 4
        },
        {
          "image": "media/mix.jpg",
          "subtitle": "最后混合翻炒加盐调味",
          "durationSeconds": 4
        }
      ]
    }
  ]
}
```

### 图片搜索关键词
- 镜头1: `eggs and tomatoes` 或 `cooking ingredients`
- 镜头2: `beat eggs bowl` 或 `whisking eggs`
- 镜头3: `cutting tomato` 或 `chopping vegetables`
- 镜头4: `scrambled eggs pan` 或 `cooking eggs`
- 镜头5: `cooking tomatoes` 或 `stir fry tomato`
- 镜头6: `mixing food wok` 或 `chinese cooking`

### 效果
- 总时长: 21秒
- 6个镜头
- 风格: 分步骤教程

---

## 示例3：产品介绍视频

### 原始内容
```
全新 AirPods Pro 2 正式发布。
搭载 H2 芯片，主动降噪效果提升2倍，支持自适应音频。
续航时间长达6小时，配合充电盒可使用30小时。
售价1899元，现已上市。
```

### 拆分方案
```json
{
  "segments": [
    {
      "id": "airpods-launch",
      "category": "产品发布",
      "source": "Apple",
      "shots": [
        {
          "image": "media/airpods-box.jpg",
          "subtitle": "全新 AirPods Pro 2 正式发布",
          "durationSeconds": 3
        },
        {
          "image": "media/h2-chip.jpg",
          "subtitle": "搭载 H2 芯片，降噪效果提升2倍",
          "durationSeconds": 4
        },
        {
          "image": "media/person-wearing.jpg",
          "subtitle": "支持自适应音频技术",
          "durationSeconds": 3
        },
        {
          "image": "media/charging-case.jpg",
          "subtitle": "续航时间长达30小时",
          "durationSeconds": 3
        },
        {
          "image": "media/price-tag.jpg",
          "subtitle": "售价1899元，现已上市",
          "durationSeconds": 3
        }
      ]
    }
  ]
}
```

### 图片搜索关键词
- 镜头1: `airpods pro` 或 `wireless earbuds white`
- 镜头2: `microchip technology` 或 `processor closeup`
- 镜头3: `person wearing earbuds` 或 `listening music`
- 镜头4: `airpods charging case` 或 `earbuds case`
- 镜头5: `price yuan` 或 `shopping technology`

### 效果
- 总时长: 16秒
- 5个镜头
- 风格: 产品宣传

---

## 示例4：新闻快讯视频

### 原始内容
```
委内瑞拉今晨发生7.3级强烈地震，首都加拉加斯震感强烈。
地震已造成至少1450人死亡，数千人受伤，多栋建筑倒塌。
中国驻委使馆确认7名中国公民在地震中不幸遇难。
国际社会纷纷表示将提供人道主义援助。
```

### 拆分方案
```json
{
  "segments": [
    {
      "id": "venezuela-earthquake",
      "category": "国际新闻",
      "source": "路透社",
      "shots": [
        {
          "image": "media/earthquake-map.jpg",
          "subtitle": "委内瑞拉今晨发生7.3级强烈地震",
          "durationSeconds": 4
        },
        {
          "image": "media/collapsed-building.jpg",
          "subtitle": "已造成至少1450人死亡，多栋建筑倒塌",
          "durationSeconds": 5
        },
        {
          "image": "media/rescue-team.jpg",
          "subtitle": "中国驻委使馆确认7名中国公民遇难",
          "durationSeconds": 5
        },
        {
          "image": "media/aid-supplies.jpg",
          "subtitle": "国际社会表示将提供人道主义援助",
          "durationSeconds": 4
        }
      ]
    }
  ]
}
```

### 图片搜索关键词
- 镜头1: `earthquake map` 或 `seismic activity`
- 镜头2: `earthquake damage building` 或 `collapsed structure`
- 镜头3: `rescue team earthquake` 或 `emergency response`
- 镜头4: `humanitarian aid` 或 `relief supplies`

### 效果
- 总时长: 18秒
- 4个镜头
- 风格: 严肃新闻

---

## 通用模式总结

### 短视频（10-20秒）
- 镜头数: 2-4个
- 每个镜头: 3-5秒
- 适用: 快讯、简短通知、产品亮点

### 中等视频（30-60秒）
- 镜头数: 6-12个
- 每个镜头: 3-5秒
- 适用: 完整新闻、教程步骤、产品介绍

### 长视频（1-3分钟）
- 镜头数: 15-30个
- 每个镜头: 3-6秒
- 适用: 深度报道、完整教程、故事讲述

## 字幕长度对照

| 字数 | 阅读时间 | 建议镜头时长 |
|-----|---------|------------|
| 10字以内 | 2秒 | 3秒 |
| 10-15字 | 3秒 | 4秒 |
| 15-20字 | 4秒 | 5秒 |
| 20-25字 | 5秒 | 6秒 |

**注意**: 字幕时长 = 阅读时间 + 1秒缓冲
