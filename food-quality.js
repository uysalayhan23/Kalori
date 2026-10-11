/* Quality flags for community-submitted records; never silently edit nutritional numbers. */
globalThis.KaloriFoodQuality=Object.freeze({
  reviewBarcodes:Object.freeze({
    "8680908020014":"Enerji ve makrolar tutarsız; kuru/pişmiş temelini kontrol edin.",
    "8691641529016":"Enerji ve makrolar arasında belirgin fark var.",
    "18921102":"Ürün adı ve besin bileşimi uyuşmayabilir.",
    "1500144801659":"Paket miktarı alanı para birimi içeriyor.",
    "5000112664478":"Karbonhidrat miktarı paket toplamı olabilir; 100 birimi doğrulanmadı.",
    "80176800":"Ürün adıyla paket miktarı çelişiyor."
  }),
  warning(food){
    if(!food||food.source!=="Open Food Facts")return "";
    const specific=this.reviewBarcodes[food.barcode];
    const q=String(food.quantity||"").trim();
    const liquid=/(?:^|\s)\d+(?:[.,]\d+)?\s*(?:ml|l|litre|lt)\b/i.test(q);
    if(liquid)return "Sıvı üründe değerlerin 100 g / 100 ml temeli doğrulanmadı. Gram hesabı uygulanmamalı."+(specific?" "+specific:"");
    return specific||"";
  },
  blocksGrams(food){return Boolean(food?.source==="Open Food Facts"&&/(?:^|\s)\d+(?:[.,]\d+)?\s*(?:ml|l|litre|lt)\b/i.test(String(food.quantity||"").trim()))}
});
