document.write('<script src="https://sdk.amazonaws.com/js/aws-sdk-2.824.0.min.js"></script>');
window.addEventListener('load', () => {

  let liffID, reslist = new Array();
  let userId;
  let a;

  liffID = '1655563753-Yb9Vdb4a';
  triggerLIFF();

  AWS.config.region = "us-east-1";
  AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: "us-east-1:669a0e47-4c7c-4189-b276-9cc9ee7e6127",
    // RoleArn: "arn:aws:dynamodb:us-east-1:138000199832:table/linebot_EATWhat_Users"
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
          reject(console.log(err));
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
    
    console.log(await result);
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
    alert('準備做資料庫更新1')
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
    alert('準備做資料庫更新2')
    docClient.update(params, function(err, data) {
        if (err) {
            console.log("Unable to update item: " + "\n" + JSON.stringify(err, undefined, 2));
            // alert(JSON.stringify(err, undefined, 2));
        } else {
            console.log("UpdateItem succeeded: " + "\n" + JSON.stringify(data, undefined, 2));
            // alert(JSON.stringify(data, undefined, 2));
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

          let res_block = document.getElementById('res_list_block');
          // let nodeFather = res_template.parentNode;
          // let node_clone = res_template.cloneNode();

          let image = document.createElement("img");
          let name = document.createElement("h4");
          let address = document.createElement("p");
          let btn = document.createElement("button");
          let cbody = document.createElement("div");
          let chead = document.createElement("div");
          let card = document.createElement("div");

          // let icon = document.createElement("i");

　　　　   name.innerHTML = res.resName;
          address.innerHTML = res.resAddress+'<br>';

          cbody.setAttribute("class", "card-body");
          chead.setAttribute("class", "card-header");
          card.setAttribute("class", "card");
          
          btn.setAttribute("type", "button");
          btn.setAttribute("class", "btn btn-danger");
          btn.setAttribute("id", res.resID);
          // btn.setAttribute("value", "delete");
          btn.innerHTML = "delete";
          btn.addEventListener('click', () => {
            if(confirm('確定刪除'+ res.resName+ ' ?')){
              reslist.splice(reslist.indexOf(parseInt(res.resID)), 1);
              updateUserResList(userId, reslist);
              location.reload()
            // console.log(reslist);
            }
          });

          image.setAttribute("class", "img-thumbnail img-fluid");
          image.src = res.resImage;

          chead.appendChild(image);
          cbody.appendChild(name);
          cbody.appendChild(address);
          cbody.appendChild(btn);
          // cbody.append(node_clone);
          card.appendChild(chead);
          card.appendChild(cbody);

          res_block.appendChild(card);

        });
        let loadgif = document.getElementById('laoding_img');
        loadgif.parentNode.removeChild(loadgif);
      }
      })

  }


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

          queryData(userId).catch(error => {
            // console.log(error);
            let error_message = document.createElement("h1");
            error_message.innerHTML ="無法從伺服器取得資料"
            document.getElementById('res_list_block').appendChild(error_message);
            console.log(error);
          });;
        })  
      }


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