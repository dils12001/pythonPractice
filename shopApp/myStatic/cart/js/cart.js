$(document).ready(function(){


    // 計算最下面 總勾選的商品價錢
    function calTotalPrice(){
        $productPriceList = $(".productPrice");
        var sum = 0;
        for(var i=0;i < $productPriceList.length;i++){
            if($($productPriceList[i]).parent().parent().parent().find(".confirm").find("span").text().trim() == "✓"){
                sum += +$($productPriceList[i]).text().slice(1);
            }
        }
        console.log("sum = ", sum);
        $("#totalPrice").text("總價 : $"+sum);
    }



    // 計算最下面 總勾選的商品個數
    function calTotalNum(){
        $productNumList = $(".productNum");
        var totalNum = 0;
        for(var i=0;i < $productNumList.length;i++){
            if($($productPriceList[i]).parent().parent().parent().find(".confirm").find("span").text().trim() == "✓"){
                totalNum += +$productNumList[i].innerHTML;
            }
        }
        console.log("totalNum = ", totalNum);
        $("#totalNum").text("共計 : "+ totalNum +" 件商品");
    }



    // 增加勾選時，判斷此時是否為"全選"
    function isAllSelect(){
        var $span = $(".confirm.isChoose").find("span")
        var flag = true;
        for(var i=0;i < $span.length;i++){
            if($($span[i]).text().trim() != "✓"){
                flag = false;
                break;
            }
        }
        if(flag){
            $('.payTheBill').find('.confirm').find("span").text("✓");
        }
    }




    // 購物車按鈕(-)
    $('.subShopping').click(function(){
        productId = $(this).attr("ga");
        console.log(productId);
        // /changeCart/0/       0是減
        $.post("/changeCart/0/", {"productId":productId}, function(returnData){
            if(returnData.status == "success"){
                // 添加成功，中間的數字(<span>)變成當前購物車的數值
                console.log(returnData.message);
                if(returnData.cartNum == 0){
                    $("."+productId).remove();
                }
                else{
                    $("#"+productId).text(returnData.cartNum);
                    $("."+productId+".productPrice").text("$"+returnData.cartPrice);
                }
                calTotalPrice();
                calTotalNum();
            }
            else if(returnData.status == 'error'){
                // 未登入，跳轉到登入介面
                console.log(returnData.message);
                window.location.href = "/login/";
            }
            else if(returnData.status == 'doNothing'){
                // 原本就沒該記錄，不做任何事
                console.log(returnData.message);
            }
        });
    });


    // 購物車按鈕(+)
    $('.addShopping').click(function(){
        productId = $(this).attr("ga");
        console.log(productId);
        // /changeCart/1/       1是加
        $.post("/changeCart/1/", {"productId":productId}, function(returnData){
            if(returnData.status == "success"){
                // 添加成功，中間的數字(<span>)變成當前購物車的數值
                console.log(returnData.message);
                $("#"+productId).text(returnData.cartNum);
                $("."+productId+".productPrice").text("$"+returnData.cartPrice);
                calTotalPrice();
                calTotalNum();
            }
            else if(returnData.status == 'error'){
                // 未登入，跳轉到登入介面
                console.log(returnData.message);
                window.location.href = "/login/";
            }
            else if(returnData.status == 'doNothing'){
                // 已經沒庫存了，不做任何事
                console.log(returnData.message);
            }
        });
    });






    $('.isChoose').click(function(){
        productId = $(this).attr("goodsId");
        console.log(productId);
        $.post("/changeCart/2/", {"productId":productId}, function(returnData){
            if(returnData.status == "success"){
                // 添加成功，中間的數字(<span>)變成當前購物車的數值
                console.log(returnData.message);
                if(returnData.isChoose){
                    $("#"+productId+"a").text("✓");
                    // 增加勾選時，判斷此時是否為"全選"
                    isAllSelect();
                }
                else{
                    $("#"+productId+"a").text(" ");
                    // 取消勾選時，一定"沒全選"
                    $('.payTheBill').find('.confirm').find("span").text(" ");
                }
                calTotalPrice();
                calTotalNum();
            }
            else if(returnData.status == 'error'){
                // 未登入，跳轉到登入介面
                console.log(returnData.message);
                window.location.href = "/login/";
            }
            else{
                // 全選 or 全部取消勾選，因ajax同時觸發，回來的順序看網路，會吃到同一個 return，所以基本上，這裡僅參考(不准)
                console.log(returnData.message);
            }
        });
    });



    $('.isChoose').on("allSelect", function(){
        productId = $(this).attr("goodsId");
        console.log(productId);
        $.post("/changeCart/3/", {"productId":productId}, function(returnData){
            // 全選 or 全部取消勾選，因ajax同時觸發
            // 回來的順序看網路，會吃到同一個 return，所以基本上，這裡僅參考(不准)
            console.log(returnData.message);
        });
    });




    $('.isChoose').on("allDisSelect", function(){
        productId = $(this).attr("goodsId");
        console.log(productId);
        $.post("/changeCart/4/", {"productId":productId}, function(returnData){
            // 全選 or 全部取消勾選，因ajax同時觸發
            // 回來的順序看網路，會吃到同一個 return，所以基本上，這裡僅參考(不准)
            console.log(returnData.message);
        });
    });




    $('.payTheBill').find('.confirm').click(function(){
        if($(this).find("span").text().trim() == "✓"){
            // 全部取消勾選
            $(this).find("span").text(" ");
            // 伺服器會處理資料庫，而這邊的頁面顯示需我們自己更新
            // 因為return的數值會錯亂
            $('.isChoose').trigger("allDisSelect");
            $(".confirm.isChoose").find("span").text(" ");
            calTotalPrice();
            calTotalNum();
        }
        else{
            // 全部勾選
            $(this).find("span").text("✓");
            $('.isChoose').trigger("allSelect");
            $(".isChoose").find("span").text("✓");

            calTotalPrice();
            calTotalNum();
        }

    });




    $('#ok').click(function(){
        var check = confirm("是否確認下單?");
        if(check){
            $.post("/saveOrder/", function(returnData){
                if(returnData.status == "success"){
                    console.log(returnData.message)
                    window.location.href = "/cart/";
                }
                else{
                    console.log(returnData.message)
                }
            });
        }
    });




    // 剛載入頁面時，算最下面的數值
    // 每次點完勾勾也需呼叫這2方法
    calTotalPrice();
    calTotalNum();









})