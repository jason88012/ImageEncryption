# Performance Index In Encryption
## Key Space
Key space代表所有密鑰的可能性空間，好的加密系統Key space必須夠大，而且密鑰必須在這個空間中隨機分佈<br />

## Correlation
Correlation代表變數之間的相關性，在影像加密中使用原影像與加密後影像個像素點作為比較
，該指標計算出來為一在[-1, 1]區間的實數，若越趨近+-1代表相關性越高，越趨近0代表相關性越低<br />

## NPCR & UACI (number of pixels change rate)
NPCR(number of pixels change rate)，UACI (unified average changing intensity)這兩項指標越高代表加密影像對抵抗Differential attack的能力越強<br />

## Histogram
直方圖表示了該加密後圖片每個灰度出現的次數<br />

## Information Entropy
Entropy用以描述影像中像素的雜亂程度，Entropy越高代表加密後圖片的雜亂度越高(從圖片可獲得的信息量越少)<br />

## Speed
即加密過程所需要的時間<br />

## Key sensitivity
該指標代表了加密後圖片對於密鑰的敏感度，計算方式為微調密鑰後計算不同密文之間的Correlation指標<br />

## Quality evaluation metrics of decrypted image
該指標代表解密後圖片與原圖的相似性，計算方式為計算原圖與解密後圖片的Correlation指標<br />