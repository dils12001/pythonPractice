$(document).ready(function(){
    $('#market').scroll(function () {
        if($(this).scrollTop() > (window.innerWidth/10*8.9)){          /* 要滑動到選單的距離 */
            $('.dropdowns').addClass('navFixed');   /* 幫選單加上固定效果 */
        }else{
            $('.dropdowns').removeClass('navFixed'); /* 移除選單固定效果 */
        }
    });


    // 分類面板 跟 排序面板 的隱藏與顯示
    $('#typediv').attr("style",'display: none;');
    $('#sortdiv').attr("style",'display: none;');

    $("#childCategory").click(function(){
        $('#typediv').attr("style",'display: block;');
        $('#sortdiv').attr("style",'display: none;');
    });

    $("#priceOrder").click(function(){
        $('#typediv').attr("style",'display: none;');
        $('#sortdiv').attr("style",'display: block;');
    });

    $("#typediv").click(function(){
        $('#typediv').attr("style",'display: none;');
    });

    $("#sortdiv").click(function(){
        $('#sortdiv').attr("style",'display: none;');
    });


    // 購物車按鈕(-)
    $('.subShopping').click(function(){
        productId = $(this).attr("ga");
        console.log(productId);
        // /changeCart/0/       0是減
        $.post("/changeCart/0/", {"productId":$(this).attr("ga")}, function(returnData){
            if(returnData.status == "success"){
                // 添加成功，中間的數字(<span>)變成當前購物車的數值
                console.log(returnData.message);
                $("#"+productId).text(returnData.cartNum);
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
        $.post("/changeCart/1/", {"productId":$(this).attr("ga")}, function(returnData){
            if(returnData.status == "success"){
                // 添加成功，中間的數字(<span>)變成當前購物車的數值
                console.log(returnData.message);
                $("#"+productId).text(returnData.cartNum);
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




});

