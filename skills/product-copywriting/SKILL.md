---
name: product-copywriting
description: Product Copywriting Skill
---

基于商品事实和知识库结果，生成门店导购话术。

- 不得编造价格、库存、优惠、尺码。
- 必须优先基于 product.get_sku 返回的事实。
- 如使用知识库内容，需要保留引用。
