let writing = false;
let tableValues = [];

jQuery(function() { 
    console.log('Ready');
    checkWifi();
    loadSettings();
    $("#wifi-form").submit(function (event) {
        event.preventDefault();
        setWifi();
      });
    $("#settings-form").submit(function (event) {
        event.preventDefault();
        saveSettings();
      });
});

async function setWifi(){
    const data = $("#wifi-form").serializeArray();
    const jsonData = data.reduce((previous, current)=>{
        previous[current.name] = current.value;
        return previous
    },{})
    await $.ajax({url: "/api/updateWifi", method:"POST", dataType : 'json',data: JSON.stringify(jsonData), contentType: 'application/json;charset=UTF-8'});
}

async function checkWifi(){
    const hasWifi = await $.ajax({url: "/api/hasWifi"});
    if(!JSON.parse(hasWifi.toLowerCase())){
        $(".wifi-section").removeAttr('hidden');
    }
}

async function loadSettings(){
    const settings = await $.ajax({url: "/api/settings", method:"GET"});
    for(let key of Object.keys(settings)){
        $(`#${key}`).val(settings[key])
    }
}

async function saveSettings(){
    const data = $("#settings-form").serializeArray();
    const jsonData = data.reduce((previous, current)=>{
        previous[current.name] = current.value;
        return previous
    },{})
    await $.ajax({url: "/api/settings", method:"POST", dataType : 'json',data: JSON.stringify(jsonData), contentType: 'application/json;charset=UTF-8'});
}
