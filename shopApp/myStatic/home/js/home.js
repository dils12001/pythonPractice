$(document).ready(function(){
    setTimeout(function(){
        swiper1();
        swiper2();
    }, 150);

})


function swiper1(){
    var mySwiper1 = new Swiper('#topSwiper', {
        direction: 'horizontal', // 水平輪播
        loop: true, // 循環播放
        speed: 500, // 圖片滑進來的速度
        autoplay: {
        delay: 5000,
        disableOnInteraction: false,
        }, // 圖片切換的間隔
        pagination: {
        el: '.swiper-pagination',
        clickable: true,
        },   // 下面有小圓點
        navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
        },
        control: true,  // 控制左右
    });
};


function swiper2(){
    var mySwiper2 = new Swiper('#swiperMenu', {
        slidesPerView: 3,
        paginationClickable: true,
        spaceBetween: 2,
        loop: false, // 不循環播放
    });
};




