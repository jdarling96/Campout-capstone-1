window.onload = function () {
    if (window.jQuery) {
      // jQuery is loaded
      console.log("jQuery has loaded!");
    } else {
      // jQuery is not loaded
      console.log("jQuery has not loaded!");
    }
  }

/* const el = $('#div1') */


const btns = [$('#btn1'),$('#btn2'),$('#btn3'),$('#btn4'),$('#btn5'),$('#btn6')];
const div = [$('.col-6.mt-5.first'),$('.col-6.mt-5.second'),$('.col-6.mt-5.third'),$('.col-6.mt-5.fourth'),$('.col-6.mt-5.fith'),$('.col-6.mt-5.six')];

for(let btn of btns){
  btn.click(function() {
      div.forEach(function(element){
        element.hide()
      });
      shw = btns.indexOf(btn)
      div[shw].show()
      $(window).scrollTop(0);
    })
  
}





