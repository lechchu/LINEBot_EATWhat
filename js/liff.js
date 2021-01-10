document.write('<script src="https://sdk.amazonaws.com/js/aws-sdk-2.824.0.min.js"></script>');
window.addEventListener('load', () => {

  let liffID, reslist = new Array();
  let userId;
  let a;

  liffID = '1655563753-Yb9Vdb4a';
  triggerLIFF();

  function deleteRes(resId){
      console.log(resId);
  }


	AWS.config.update({
	  region: "us-east-1",
	  //endpoint: 'http://localhost:8000',
	  // accessKeyId default can be used while using the downloadable version of DynamoDB. 
	  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
	  accessKeyId: "ASIASAILT6CMBJUQQIZC",
	  // secretAccessKey default can be used while using the downloadable version of DynamoDB. 
	  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
	  secretAccessKey: "N3m54MOEtCSGD37hj0ywW/E8o1X2EoM3oZLRlWzg",
    sessionToken: "FwoGZXIvYXdzENb//////////wEaDIsZhJiPjmlA9zYQLSLIAUBpq1nGm7Wt5phTpbTmjKF8o3oOdSgNwCSiBoME1ysGNwfgu5jTWxzmQCSd6gRhyFI3H34dTPlqXkVZvxmFZ6fpijP3kiq2y5aPEHJ0ycl3Knpnvfr0rS5g2I89yt4RsXdpaxSVHDGhi6dZ6ZGjEFTz+hv7xQ1bQGHBH1rsBydOp7ncQvIGqKYVUDPwz0eK/MbmJ7T072HK+8XNUa/1enh6LqaaXhu+/AV5nfnEiXzHKkycJpZAwtrnUi5Jn3G+aMtKap5PiwoTKIHk6/8FMi0/827FdzXXcQYjKGn8g9MKMPVujAR4GSZlfFreOTmDI5l+Q+so8GxOYxmxzEA="
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
	
    const qresult = new Promise((resolve, reject) => {     
      docClient.query(params, function (err, data) {
          resolve(data);
          reject(err);
        })
      });

    result = await qresult;
    if(await result['Count'] === 0){
      initData(keyword);
      return;
    }
    reslist = result['Items'][0]['resList'];
    console.log(reslist);
    // console.log(result['Items']);

    loadResList();

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
          queryData(userId);
      }
    });
  }

  function updateUserResList(userId, newlist){

    var params = {
        TableName:"linebot_EATWhat_Users",
        Key:{
            "userId": userId
        },
        UpdateExpression: "set resList = :nrl",
        ExpressionAttributeValues:{
            ":nrl":newlist,

        },
        ReturnValues:"UPDATED_NEW"
    };

    docClient.update(params, function(err, data) {
        if (err) {
            console.log("Unable to update item: " + "\n" + JSON.stringify(err, undefined, 2));
        } else {
            console.log("UpdateItem succeeded: " + "\n" + JSON.stringify(data, undefined, 2));
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

          // console.log(reslist.includes(parseInt(res.resID)));
          if(!reslist.includes(parseInt(res.resID))){
            return;
          }

          let res_template = document.getElementById('res_temp');
          let nodeFather = res_template.parentNode;
          let node_clone = res_template.cloneNode();
          let image = document.createElement("img");
          let name = document.createElement("h5");
          let address = document.createElement("span");
          let btn = document.createElement("input");

　　　　   name.innerHTML = res.resName;
          address.innerHTML = res.resAddress;

          btn.setAttribute("type", "button");
          btn.setAttribute("id", res.resID);
          // btn.setAttribute("onClick", "deleteRes(this.id)");
          btn.setAttribute("value", "delete");
          btn.addEventListener('click', () => {
            if(confirm('確定刪除 %s？', res.Name)){
              reslist.splice(reslist.indexOf(parseInt(res.resID)), 1);
              updateUserResList(userId, reslist);
              location.reload()
            // console.log(reslist);
            }
          });

          image.setAttribute("class", "fa fa-wrench");
          image.src = res.resImage;
          node_clone.appendChild(image);
          node_clone.appendChild(name);
          node_clone.appendChild(address);
          node_clone.appendChild(btn);

          nodeFather.appendChild(node_clone);

        });
      }
      })
     
    
  }

  // queryData("1");
  // console.log(getResCount());

  function triggerLIFF() {


    // LIFF init
    liff.init({
      liffId: liffID
    }).then(() => {
      
      // 取得基本環境資訊
      // 參考：https://engineering.linecorp.com/zh-hant/blog/liff-our-latest-product-for-third-party-developers-ch/
      let language, version, isInClient, isLoggedIn, os, lineVersion, userName, userImage, user_profile;

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
          queryData(userId);
          
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