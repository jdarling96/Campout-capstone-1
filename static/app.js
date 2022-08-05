/* const el = $('#div1') */
let getUrl = window.location;
let baseUrl =
  getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split("/")[0];

const $btns = [
  $("#btn1"),
  $("#btn2"),
  $("#btn3"),
  $("#btn4"),
  $("#btn5"),
  $("#btn6"),
];
const $div = [
  $(".col-6.mt-5.first"),
  $(".col-6.mt-5.second"),
  $(".col-6.mt-5.third"),
  $(".col-6.mt-5.fourth"),
  $(".col-6.mt-5.fith"),
  $(".col-6.mt-5.six"),
];

for (let btn of $btns) {
  btn.click(function () {
    $div.forEach(function (element) {
      element.hide();
    });
    shw = $btns.indexOf(btn);
    $div[shw].show();
    $(window).scrollTop(0);
  });
}

$("#saved-sites").click(function () {
  getSaves();

  $("#saved-sites")
    .off("click")
    .on("click", function () {
      if ($("#saved-campsites-container").is(":visible")) {
        $("#saved-campsites-container").hide();
        $("#save-data-container").css("height", "100%");
      } else if ($("#recommend-campsites-container").is(":visible")) {
        $("#save-data-container").css("height", "auto");
      } else {
        $("#saved-campsites-container").show();
      }
    });
});

async function getSaves() {
  let res = await axios.get(`${baseUrl}api/users/account/saved`);

  if (res.data.length === 0) {
    $("#saved-sites").off("click");
    return;
  }
  if (res.data.length >= 3) {
    $("#save-data-container").css("height", "auto");
  }

  displaySaves(res.data);
}

function displaySaves(data) {
  data.forEach((element) => {
    let { facility_name, facility_photo, facility_type, state } = element;
    if (facility_photo === "http://www.reserveamerica.com/images/nophoto.jpg") {
      facility_photo = "/static/images/generic-campsite.jpg";
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
     `
    );

    $("#saved-campsites-container").append($display);
  });
  $("#saved-campsites-container").show();
}

$("#recommend-sites").click(function () {
  getRecommend();

  $("#recommend-sites")
    .off("click")
    .on("click", function () {
      if ($("#recommend-campsites-container").is(":visible")) {
        $("#recommend-campsites-container").hide();
        $("#save-data-container").css("height", "100%");
      } else if ($("#saved-campsites-container").is(":visible")) {
        $("#save-data-container").css("height", "100%");
      } else {
        $("#recommend-campsites-container").show();
        $("#save-data-container").css("height", "auto");
      }
    });
});

async function getRecommend() {
  let res = await axios.get(`${baseUrl}api/user/account/recommend`);

  if (res.data.length === 0) {
    $("#recommend-sites").off("click");
    return;
  }
  $("#save-data-container").css("height", "auto");
  displayRec(res.data);
}

function displayRec(data) {
  userId = data[0].user_id;
  data[1].forEach((element) => {
    let {
      "@facilityName": facility_name,
      "@faciltyPhoto": facility_photo,
      "@state": state,
      "@contractType": facility_type,
      "@sitesWithAmps": amps,
      "@sitesWithPetsAllowed": pets,
      "@sitesWithSewerHookup": sewer,
      "@sitesWithWaterHookup": water,
      "@sitesWithWaterfront": waterfront,
      "@longitude": landmark_long,
      "@latitude": landmark_lat,
    } = element;

    if (facility_photo !== "/images/nophoto.jpg") {
      facility_photo = `http://www.reserveamerica.com${facility_photo}`;
    } else {
      facility_photo = "/static/images/generic-campsite.jpg";
    }

    const $display = $(
      `<div class="row"> 
       <div class="col">
       <img class="img-thumbnail mb-2" src="${facility_photo}" alt="Picture of campsite." srcset="">
       </div>
       </div>
       <div class="row">
       <div class="col">
          <p class="h6">Park: ${facility_name}</p>
          <form action="/search/save/${facility_name}" method='POST'>
          <input name="facility_photo" type="hidden" value="${facility_photo}">
          <input name="facility_name" type="hidden" value="${facility_name}">
          <input name="state" type="hidden" value="${state}">
          <input name="facility_type" type="hidden" value="${facility_type}">
          <input name="amps" type="hidden" value="${amps}">
          <input name="pets" type="hidden" value="${pets}">
          <input name="water" type="hidden" value="${water}">
          <input name="sewer" type="hidden" value="${sewer}">
          <input name="waterfront" type="hidden" value="${waterfront}">
          <input name="eq_length" type="hidden" value="{{result_set['@eqplen']}}">
          <input name="landmark_lat" type="hidden" value="${landmark_lat}">
          <input name="landmark_long" type="hidden" value="${landmark_long}">
          <button type="submit" class="btn btn-outline-secondary btn-sm mt-1"><i class="fa-solid fa-bookmark"></i></button>
          </form>
          </div>
      <div class="col">  
          <p class="h6">State: ${state}</p>
          <p class="h6 mb-2">Type: ${facility_type}</p>
          </div>
          <div class="col">
          <p class="h6 mb-2">Type: ${amps}</p>
          <p class="h6 mb-2">Type: ${pets}</p>
          <p class="h6 mb-2">Type: ${sewer}</p>
          <p class="h6 mb-2">Type: ${water}</p>
          <p class="h6 mb-2">Type: ${waterfront}</p>
          </div>
          </div>
        `
    );

    $("#recommend-campsites-container").append($display);
  });
  $("#recommend-campsites-container").show();
}

