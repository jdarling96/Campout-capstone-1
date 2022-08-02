

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

$('#saved-sites').click(function(){
  getSaves()
  

  $('#saved-sites').off('click').on('click', function(){
    
    if($('#saved-campsites-container').is(":visible")) {
      $('#saved-campsites-container').hide();
    }
    else {
      $('#saved-campsites-container').show();

    }
      
  
    
  });
  
})

async function getSaves() {
  let res = await axios.get('http://127.0.0.1:5000/api/users/account/saved')
  console.log(res.data)
  if(res.data.length === 0){
    $('#saved-sites').off('click')
    return
  }
  displaySaves(res.data)
}

function displaySaves(data) {
  
  data.forEach(element => {
    let {facility_name,facility_photo, facility_type, state} = element
    if(facility_photo === "http://www.reserveamerica.com/images/nophoto.jpg"){
      facility_photo = "/static/images/generic-campsite.jpg"
    }
    
    const $display = $(
      `<div class="row"> 
       <div class="col">
       <img class="img-thumbnail mb-2" src="${facility_photo}" alt="Picture of campsite." srcset="">
       </div>
       </div>
       <div class="row">
       <div class="col m-2">
          <p class="h6">Park: ${facility_name}</p>
          <p class="h6">State: ${state}</p>
          <p class="h6 mb-2">Type: ${facility_type}</p>
          <form action="/api/user/account/saved/${facility_name}/delete" method='POST'>
          <button type="submit" class="btn btn-outline-danger btn-sm mt-1"><i class="fa-solid fa-trash"></i></button>
          </form>
       </div>
      
     </div>
     `);
    
    $('#saved-campsites-container').append($display)
  
  });
  $('#saved-campsites-container').show()

 
}


$('#recommend-sites').click(function(){
  getRecommend()
})

async function getRecommend(){
  let res = await axios.get('http://127.0.0.1:5000/api/user/account/recommend')
  console.log(res.data)

  displayRec(res.data)
}

function displayRec(data) {
  
  data.forEach(element => {
    let {facility_name,facility_photo, facility_type, state} = element
    if(facility_photo === "http://www.reserveamerica.com/images/nophoto.jpg"){
      facility_photo = "/static/images/generic-campsite.jpg"
    }
    
    const $display = $(
      `<div class="row"> 
       <div class="col">
       <img class="img-thumbnail mb-2" src="${facility_photo}" alt="Picture of campsite." srcset="">
       </div>
       </div>
       <div class="row">
       <div class="col m-2">
          <p class="h6">Park: ${facility_name}</p>
          <p class="h6">State: ${state}</p>
          <p class="h6 mb-2">Type: ${facility_type}</p>
          <form action="/api/user/account/saved/${facility_name}/delete" method='POST'>
          <button type="submit" class="btn btn-outline-danger btn-sm mt-1"><i class="fa-solid fa-trash"></i></button>
          </form>
       </div>
      
     </div>
     `);
    
    $('#saved-campsites-container').append($display)
  
  });
  $('#saved-campsites-container').show()

 
}






