# Back up HW in NTHU eeclass

## 目的

![](/images/demo.png)

自動下載**歷屆作業**的檔案。<br>
> 只能下載這個區塊的檔案，被放在其他地方的檔案作者抓不到QwQ

## [0] 使用限制

### [0.1] 系統限制
Only Windows
****

## [1] 前置作業

### [1.1] 確認 Google Chrome 版本
#### [step1] 點選右上角的3顆點點 -> 說明 -> 關於 Google Crome
![step1](/images/chrome_version_step1.png)


#### [step2] 可以在下圖方框中查看目前使用的 $Google$ 版本 <br>
  e.g. 作者現在的版本是 **114.5735.199** ，也就是 114版
![step2](/images/chrome_version_step2.png)

#### [step3] 下載本專案

根據自己的Google版本，點選對應的分支 <br>
> 作者是114版，因此這邊選擇 v114，v114 代表version 114 <br>
> 請根據自己的版本選擇對應的資料夾

![step3](/images/chrome_version_step3.png)

#### [step4] 點進分支後下載

![step4](/images/chrome_version_step4.png)

點選綠色的code按鈕 -> Download ZIP -> 解壓縮該檔案 -> 把它放到 Download 資料夾以外的地方 
> 這步驟非常重要!

### [1.2] 紀錄登入 $eeclass$ 時使用的 $cookie$

#### [step1] 登入eeclass
  
![step1](/images/cookie_step1.png)


#### [step2] 在頁面上按壓鍵盤 ctrl + shift + i -> 選擇 Network欄位 
  
![step2](/images/cookie_step2.png)


#### [step3] 刷新頁面會跑出載入頁面時使用的資料
  
![step3](/images/cookie_step3.png)


#### [step4] 紀錄cookie
  
刷新eeclass頁面，Network欄位會刷新資料 <br>
點選dashboard -> Cookies -> 找到PHPSESSID <br>
這個值請紀錄下來，稍後會用到。**千萬不要外流**，自己知道就好，

![step4](/images/cookie_step4.png)

#### [step5] 將參數放入 **env.json**

如下圖所示，將env.json打開 <br>
把剛剛得知的cookie放在value欄位

![step5](/images/env.png)

### [1.3] 設定下載路徑

#### [step1] 點擊電腦下載檔案後被放置的資料夾
  
![step1](/images/download_step1.png)

#### [step2] 在資料夾內部點擊滑鼠右鍵 -> 點擊內容

![step2](/images/download_step2.png)

#### [step3] 紀錄您電腦的下載路徑

![step3](/images/download_step3.png)

>以這張圖來說，作者的下載路徑是 C:\Users\User\Downloads

#### [step4] 將參數放入 **env.json**

![step4](/images/download_step4.png)
> 注意 !!! 要將下載路徑中全部的單斜線 ( \\ ) 換成雙斜線 ( \\\\ ) <br>
>  比方說 : C:\Users\User\Downloads -> C:\\\Users\\\User\\\Downloads

### [1.4] 將Download底下的文件全部清光

* 如下圖
![step1](/images/clean_download.png)


## [2] 開始使用

#### [step1] 打開專案資料夾

直接點擊 `main.exe` 這個檔案就會開始執行。執行過程請不要操控滑鼠，會出大事。

![Alt text](/images/main_exe.png)

如果過多檔案下載-掃描病毒失敗，詳見底下的 [修復Bug3.1] 內容。

如果執行後發現會有個視窗瞬間跳出來又關閉，並且程式停止，詳見底下的 [修復Bug3.2] 內容。

[step2] 程式結束後檔案會在 `download_file` 資料夾之下

![](/images/download_file.png)

## [3] 修復 Bug

### [3.1] 下載-掃描病毒失敗

根據這篇文章的內容[修復 Google Chrome 病毒掃描失敗錯誤的 5 大方法](https://www.a7la-home.com/zh-TW/top-ways-to-fix-virus-scan-failed-error-in-google-chrome) 選擇第四個方法執行。

### [3.2] Chromedriver閃退、自動關閉

順利執行的情況下，Chrome driver會一直跳轉頁面，直到全部的檔案下載完畢。
順勢閃退、自動關閉，代表您選擇的Chrome driver和您現在的Google版本不一致，請重新安裝正確的版本。
