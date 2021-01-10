document.write('<script src="https://sdk.amazonaws.com/js/aws-sdk-2.824.0.min.js"></script>');
window.addEventListener('load', () => {

  let liffID, qresult;
  let a;

  liffID = '1655563753-Yb9Vdb4a';
  triggerLIFF();


	AWS.config.update({
	  region: "us-east-1",
	  //endpoint: 'http://localhost:8000',
	  // accessKeyId default can be used while using the downloadable version of DynamoDB. 
	  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
	  accessKeyId: "ASIASAILT6CMIE3Z5UDR",
	  // secretAccessKey default can be used while using the downloadable version of DynamoDB. 
	  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
	  secretAccessKey: "BLdkUBf2xudKPJG35TNrHrA+6gqPLSgPWmxyQfy2",
    sessionToken: "FwoGZXIvYXdzENP//////////wEaDB6muXZ0vYSCYBNZ2SLIARNpXruQ5kUtk6wqhqzkZ/2f4wC1swwGZT5Ihdr9S+v+w8dECU0CvIWxYcUBic6QeBgSYV6clHtXaX12O439z239E5wlMtlNpvHmi2Gp/fpdKrRyd3C4b2cHQGvPFRAZuyiCoqN2EI0rkPW5sRvolYWsNvI+QA99Y/cGYs1wVcwX88Wl66g3ShQLshaLrOJEMJKrni/6EnKo47YUYp3UP/k9PTviY5WNQ1wpeHah+hm07Q5c9HQuJIXEm3K/oqJSMAq3cQdK6FpqKI2W6/8FMi3LSgxEW32ALweiSQBbawaAxPUZaS4jWVWfksb+N7BDDbCRRuaLRz88mrD4G2k="
  });
  
  var docClient = new AWS.DynamoDB.DocumentClient();

  async function queryData(keyword) {
    var params = {
      TableName: "linebot_EATWhat_Users",
      KeyConditionExpression: "#uid = :kw",
      ExpressionAttributeNames: {
              "#uid": "userId",
      },
      ExpressionAttributeValues: {
          ":kw": keyword
      }
    };
	
    const result = new Promise((resolve, reject) => {     
      docClient.query(params, function (err, data) {
          resolve(data);
          reject(err);
        })
      });
    let a = await result;
    result.then(() => {
      console.log(result);
    })
    console.log(a['Count'])
    if(a['Count'] === 0){
      initData(keyword);
    }
    const qcount = result['Count'];

  }

  async function getResCount(){
    let  ans, result;
    var params = {
      TableName: "linebot_EATWhat_DB",
    };

    result = new Promise((resolve, reject) => {     
      docClient.scan(params, function (err, data) {
          resolve(data);
          reject(err);
        })
      });
    
    
    a = await result;
    console.log(a);
    return await result;
  }


  function initData(userId){
    let resCount = 50;
    let resList = new Array();

    for(i=0;i<resCount;i++){
      　resList.push(i+1);
    }

    var params = {
      TableName :"linebot_EATWhat_Users",
      Item:{
          "userId": userId,
          "resList": resList
      }
    };

    docClient.put(params, function(err, data) {
      if (err) {
        console.log("Unable to add item: " + "\n" + JSON.stringify(err, undefined, 2));
      } else {
          console.log("PutItem succeeded: " + "\n" + JSON.stringify(data, undefined, 2));
      }
    });
  }

  async function loadResList(){

    var params = {
      TableName: "linebot_EATWhat_DB",
    };

   
    docClient.scan(params, function (err, data) {
      if (err) {
        console.log("Unable to scan the table: " + "\n" + JSON.stringify(err, undefined, 2));
      } else {
        // Print all the movies
        console.log("Scan succeeded. " + "\n");
        data.Items.forEach(function(res) {
          let res_template = document.getElementById('res_temp');
          let nodeFather = res_template.parentNode;
          let node_clone = res_template.cloneNode();
          // content = res_template.innerHTML;
          // console.log(content.childElementCount);
          let image = document.createElement("img");
          let icon = document.createElement("span");
          let name = document.createElement("h5");
          let address = document.createElement("span");
          icon.setAttribute("class", "fa fa-wrench");
　　　　   name.innerHTML = res.resName;
          address.innerHTML = res.resAddress;

          image.setAttribute("class", "fa fa-wrench");
          image.src = res.resImage;
          node_clone.appendChild(image);
          // node_clone.appendChild(icon);
          node_clone.appendChild(name);
          node_clone.appendChild(address);
          // node_clone.childNodes[0][0][1].textContent = res.resName;
          // node_clone.childNodes[0][0][2].textContent = res.resAddress;
          // node_clone.removeAttribute('id');
          // node_clone.innerHTML = content;
          nodeFather.appendChild(node_clone);
            // document.getElementById('textarea').innerHTML += movie.year + ": " + movie.title + " - rating: " + movie.info.rating + "\n";
        });
      }
      })
     
    
  }

  // queryData("1");
  console.log(getResCount());
  // let count = await getResCount();
  // console.log(count);
  // 執行範例裡的所有功能
  function triggerLIFF() {


    // LIFF init
    liff.init({
      liffId: liffID
    }).then(() => {
      
      // 取得基本環境資訊
      // 參考：https://engineering.linecorp.com/zh-hant/blog/liff-our-latest-product-for-third-party-developers-ch/
      let language, version, isInClient, isLoggedIn, os, lineVersion, userId, userName, userImage, user_profile;

      language = liff.getLanguage(); // String。引用 LIFF SDK 的頁面，頁面中的 lang 值
      version = liff.getVersion(); // String。LIFF SDK 的版本
      isInClient = liff.isInClient(); // Boolean。回傳是否由 LINE App 存取
      isLoggedIn = liff.isLoggedIn(); // Boolean。使用者是否登入 LINE 帳號。true 時，可呼叫需要 Access Token 的 API
      os = liff.getOS(); // String。回傳使用者作業系統：ios、android、web
      lineVersion = liff.getLineVersion(); // 使用者的 LINE 版本

		  if(!isLoggedIn) {
          liff.login({
            redirectUri: location.href
          });
      }


      if(isLoggedIn) {
        liff.getProfile().then(profile => {
          user_profile = profile;
          userId = profile['userId'];
          userName = profile['displayName'];
          userImage = profile['pictureUrl'];
          document.getElementById('profile_image').src=userImage;
          document.getElementById('userName').textContent=userName;
          loadResList();
        })
    
      }

      // profile = getProfile();
      userId = liff.getContext()['userId'];


 
      // const btnProfile = document.getElementById('profile');
      // btnProfile.addEventListener('click', () => {
      //   // 先確認使用者是登入狀態
      //       const outputContent = document.getElementById('result-info');
      //       outputContent.value = `${JSON.stringify(user_profile)}`
      //       console.log(userName);
      //       console.log(userId);
      //       console.log(qresult);
      //       queryData(userId);
        
      // });





      // 關閉 LIFF
      // const btnClose = document.getElementById('closeLIFF');
      // btnClose.addEventListener('click', () => {
      //   // 先確認是否在 LINE App 內
      //   if(isInClient) {
      //     liff.closeWindow();
      //   }
      // });

    }).catch(error => {
		  console.log(error);
    });
  
  }
})