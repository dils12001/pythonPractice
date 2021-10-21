$(document).ready(function(){
    $("#showMyOrders").click(function(){
        $.post("/showMyOrders/", function(returnData){
            if(returnData.status == "success"){
                console.log(returnData.message);
                // 先清空所有內容，避免顯示重複訂單
                $("#allOrders").text("");
                for(var i=0;i < returnData.orderData.length;i++){
                    if(returnData.orderData[i]["progress"] == 1){
                        progress = "運送中";
                    }
                    else if(returnData.orderData[i]["progress"] == 2){
                        progress = "待取貨";
                    }
                    else if(returnData.orderData[i]["progress"] == 3){
                        progress = "已結單";
                    }
                    $("#allOrders").append('<div class="oneOrder"><div><span class="orderId">orderId: ' + returnData.orderData[i]["orderId"] + '</span><span class="orderProgress">目前狀態: '+ progress +'</span><span class="orderDetail" orderId="a' + returnData.orderData[i]["orderId"] + '">詳細資訊</span>');
//                    console.log(returnData.orderData[i]["orderId"])
                }
                // 為剛加上去的span，添加點擊事件
                orderDetailClick();
            }
            else if(returnData.status == "doNothing"){
                // 沒任何訂單，待測試樣式!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                $("#allOrders").append("<span>您目前沒有任何訂單喔</span>");
                console.log(returnData.message);
            }
            else{
                // returnData.status == "error"
                console.log(3);
                console.log(returnData.message);
                window.location.href = "/login/";
            }
        });
    });

//    $("#allOrders").append('<div class="oneOrder"><span class="orderId">orderId: 12354645</span><span class="orderProgress">目前狀態: 運送中</span><span class="orderDetail">詳細資訊</span></div>');



    function orderDetailClick(){
        $(".orderDetail").click(function(){
            $orderId = $(this).attr("orderId");
            console.log($orderId);
            // 先新增一個可識別id 的標籤
            // $.post裡不能用 $(this)
            // 若已存在表示，這次點選是要隱藏詳細資訊，直接刪除元素
            if($("#"+$orderId).html() != undefined){
                $("#"+$orderId).remove();
                console.log('break~');
                return;
            }
            $(this).parent().parent().append('<div class="detail" id="' + $orderId + '"></div>');
            $.post("/showOrderDetail/" + $orderId + "/", function(returnData){
                console.log($orderId);
                if(returnData.status == "success"){
                    console.log(returnData.message);

                    detailList = returnData.orderDetailList;
                    $("#"+$orderId).append("<ul></ul>")
                    for(var i=0;i < detailList.length;i++){
                        productId = detailList[i]["fields"]["productId"];
                        productImg = detailList[i]["fields"]["productImg"];
                        productName = detailList[i]["fields"]["productName"];
                        productNum = detailList[i]["fields"]["productNum"];
                        totalPrice = detailList[i]["fields"]["totalPrice"];
                        orderId = detailList[i]["fields"]["orderId"];

                        $("#"+$orderId).find("ul").append('<li class="menuList ' + productId + '"><a href="#"><img src="' + productImg + '" alt=""></a><div class="rightDiv"><a href="#"><p>' + productName + '</p><span class="' + orderId + ' productPrice ' + productId + '">$' + totalPrice + '</span></a><section><span id="' + productId + '" class="' + orderId + ' productNum">數量: ' + productNum + '</span></section></div></li>');
                    }
                    priceList = $("#"+$orderId).find(".productPrice");
                    numList = $("#"+$orderId).find(".productNum");
                    priceSum = 0;
                    numSum = 0;
                    for(var i=0; i < priceList.length;i++){
                        priceSum += Number($(priceList[i]).text().substr(1));
                        numSum += Number($(numList[i]).text().substr(4));
                    }
                    $("#"+$orderId).find("ul").append('<li class="payTheBill"><p><span id="totalNum">共計 : ' + numSum + ' 件商品</span><span id="totalPrice" style="text-align: center;">總價 : $' + priceSum + '</span><a class="cancel" id="b' + orderId + '">取消訂單</a></p></li></ul>');

                    // "取消訂單"的按鈕事件
                    $("#b"+$orderId.substr(1)).click(function(){
                        // !!!這裡要用 $(this).attr("id")!!!
                        // 不能使用 #b"+$orderId.substr(1) 去拿取orderId
                        // 因為先前的確是依$orderId這個變數，識別按鈕添加點擊方法
                        // 但它們每次點擊時，才來跑這裡面的方法，這是$orderId可能已經變了
                        // $orderId在每次點詳細資訊時，都會更改
                        $.post("/deleteOrder/", {'orderId': $(this).attr("id").substr(1)}, function(returnData){
                            console.log(returnData.message);
                            $("#a"+returnData.orderId).parent().remove();
                        });
                    });

                }
                else if(returnData.status == "doNothing"){
                    console.log(returnData.message);
                }
                else{
                    // returnData.status == "error"
                    console.log(returnData.message);
                    window.location.href = "/login/";
                }
            });// post尾巴



        });
    }









});

