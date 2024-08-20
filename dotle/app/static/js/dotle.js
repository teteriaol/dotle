addEventListener('dragstart',function(e){e.preventDefault()});
document.addEventListener("DOMContentLoaded", function() {
$(document).ready(function() {
    $.ajax({
        url: '/api/get_heroes/',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            const heroList = response.heroesser;
            const heroData = JSON.parse(heroList);
            processHeroData(heroData);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});
$(document).ready(function() {
  $(".dottleform").submit(function(event) {
    event.preventDefault(); 
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(), 
      success: function(data) {
        $.fn.reverse = [].reverse
        let attempts = data.attempts;
        let attemptNumber = Object.keys(attempts).length - 1;
        let attempt = attempts[attemptNumber];
        // console.log(attempts[attemptNumber].Adjectives);
        let isGuessed = data.is_guessed;
        let tableHeader = $('.table-header');
        let goodJobText = $(`<h1 class="countdown__heading">Good job! Today's hero - ${attempt.Name}</h1>`);
        let inputContainer = $('.input__container');
        let inputWrapper = $('.input__wrapper');
        if (isGuessed == true){
          $(inputWrapper).fadeOut("slow", function(){
            inputContainer.replaceWith(goodJobText);
            $(".inputContainer").hide().fadeIn("slow");
          });
        } else {
          $(".dottleform :input").prop("disabled", false);
        }
        
        adjString = '';
        _l = attempt.Adjectives;
        for (var key in _l) {
          let _s = _l[key].style;
          let _n = _l[key].Name;
          adjString = adjString.concat(`<div class="role__container ${_s}">${_n}</div>`);
        }

        simString = ''
        _l = attempt.SimilarHeroes;
        for (var key in _l) {
          let _s = _l[key].style;
          let _n = _l[key].Name;
          let _img =`<img class="dotle__icon icon__minimap" src="https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/icons/${_l[key].CodeName}.png" alt="${_n}">`;
          if (_n == "No Information"){
            _img = _n
          }
          simString = simString.concat(`<div class="role__container ${_s}">${_img}</div>`);
        }

        roleString = '';
        rolevelString = '';
        _l = attempt.Role;
        for (var key in _l) {
          let _s = _l[key].style;
          let _n = _l[key].Name;
          let _r = _l[key].Rolelevels;
          roleString = roleString.concat(`
          <div class="roles__container ${_s}">
              <div class="dotle__icon ${_n}" rolename="${_n}"></div>${'<div class="role-level"></div>'.repeat(_r.length)}
          </div>
          `);
        }
      
        let newattempt = $(`<li class="table-row">
          <div class="col hero_name">
              <span class="hero_text">${attempt.Name}</span>
              <img src="https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${attempt.CodeName}.png" alt="${attempt.Name}" width="160">
          </div>
          <div class="col ${attempt.AttributePrimary.style} "><!-- ${attempt.AttributePrimary.Name} --><div class="dotle__icon icon__attribute ${attempt.AttributePrimary.Name}"></div></div>
          <div class="col col-1"> 
            ${roleString}               
          </div>
          <div class="col col-2 ${attempt.Team.style}"><!-- ${attempt.Team.Name} --><div class="dotle__icon icon__team ${attempt.Team.Name}"></div> </div>
          <div class="col col-3 ${attempt.AttackType.style}"><!-- ${attempt.AttackType.Name} --><div class="dotle__icon icon__atype ${attempt.AttackType.Name}"></div></div>
          <div class="col col-4">
              ${simString}
          </div>
          <div class="col col-4">
              ${adjString}
          </div>
        </li>`);
        newattempt.insertAfter(tableHeader);

        const heroCards = Array.from(document.querySelectorAll('.col')).slice(0, 7);
        setTimeout(function() {

          heroCards.forEach(function(el){
            el.style.transform = "rotateY(360deg)";
          });
            }, 100);
        $(".dottleform")[0].reset();
        $(".dottleform :input").select();
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});

$(document).ready(function() {
  $("#reroll_hero").click(function() {
    $.ajax({
      url: '/api/reroll_hero/',
      type: 'GET',
      success: function(response) {
        if (response.reload_needed){
          location.reload();
        }
      },
      error: function(error) {
          console.error(error);
      }
    });
  });
});

function processHeroData(heroData) {
  let heroNames = heroData.map(hero => ({
    Name: hero.fields.Name,
    CodeName: hero.fields.CodeName,
    Aliases: hero.fields.NameAliases
  }));
  let input = document.getElementById("id_hero_field");
  let list = document.querySelector(".list");
  let button = document.querySelector('.input__button')
  let attempts = document.querySelectorAll('.attempts_table .table-row .hero_name');
  let usedHeroes = [];
  let currentIndex = -1;
  const observer = new MutationObserver(handleListChange)
  if(list != null){
  observer.observe(document.querySelector('.list'), {
    childList: true,
    subtree: true, 
  });
}

  attempts.forEach((v) => {
    usedHeroes.push(v.innerText);
  });
  if (input!=null) {
  input.addEventListener("keydown", (e) => {
    let names = document.querySelectorAll(".list__name");
    if (13 == e.keyCode) {
      e.preventDefault();
      let _j = document.querySelector(".list-items");
      if (_j && currentIndex == -1) {
        input.value = _j.innerText;
        usedHeroes.push(_j.innerText);
        removeElements();
        $(".dottleform").submit();
        $(".dottleform")[0].reset();
        $(".dottleform :input").prop("disabled", true);
      }
      else if(_j){
        input.value=names[currentIndex].textContent;
        removeElements();
        $(".dottleform").submit();
        $(".dottleform")[0].reset();
        $(".dottleform :input").prop("disabled", true);
      }
    } else if (13 == e.keyCode && names.length == 1){
      heroNames.forEach((hero) => {
        if(hero.Name == input.value) {
          $(".dottleform").submit();
          $(".dottleform")[0].reset();
          $(".dottleform :input").prop("disabled", true);
        }
      });
    }
    else if(40 == e.keyCode){
      currentIndex = Math.min(currentIndex + 1, names.length - 1);
      if(list.scrollTop<currentIndex*318){
        list.scrollTop+=106;
      }
    }else if (e.keyCode === 38) {
      currentIndex = Math.max(currentIndex - 1, -1);
      if(list.scrollTop>currentIndex<318){
        list.scrollTop-=106;
      }
    }
    if (currentIndex > -1) {
      let _j = document.querySelectorAll(".list-items");
      input.value = names[currentIndex].textContent;
      if(currentIndex!=0){
        _j[currentIndex-1].style.backgroundColor='';
      }
        _j[currentIndex].style.backgroundColor='#dddddd';
      if(currentIndex!=names.length-1){
        _j[currentIndex+1].style.backgroundColor='';
      }
    }
  });

  input.addEventListener("input", (e) => {
    removeElements();

    const lowerInputValue = input.value.toLowerCase();
    let matchingCount = 0;
    for (let i of heroNames) {
      const lowerHeroName = i.Name.toLowerCase();
      let lowerHeroAliases = i.Aliases.split(',').map(word => word.trim().toLowerCase());
      if (usedHeroes.includes(i.Name)){
        continue;
      }

      if (nameContains(lowerHeroName, lowerInputValue) || lowerHeroAliases.some(alias => alias.includes(lowerInputValue)) && input.value !== "") {
        matchingCount++;

        let listItem = document.createElement("li");
        listItem.classList.add("list-items");
        listItem.style.cursor = "pointer";

        listItem.addEventListener("click", () => {
          input.value = i.Name;
          removeElements();
        });

        let imgElement = document.createElement("img");
        imgElement.src = `https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${i.CodeName.replace('npc_dota_hero_', '')}.png`;
        imgElement.classList.add("list__icon");
        imgElement.alt = `${i.Name}_icon`;
        imgElement.width = 150;
        imgElement.height = 84;

        let nameSpan = document.createElement("span");
        nameSpan.innerHTML = highlightMatchingPart(i.Name, input.value);
        nameSpan.classList.add("list__name");

        listItem.appendChild(imgElement);
        listItem.appendChild(nameSpan);
        list.appendChild(listItem);
        list.style.height =`${document.querySelectorAll('.list-items').length*106}px`
      }
    }

    if (matchingCount === 0 && input.value.length > 0) {
      input.style.backgroundColor = "#9a564b";
      button.style.backgroundColor = '#656363';
      button.disabled = true;
    } else {
      button.style.backgroundColor = "rgba(0, 0, 0, 0)";
      button.disabled = false;
      input.style.backgroundColor = '#444444';
    }
  });
  }

  function removeElements() {
    let items = document.querySelectorAll(".list-items");
    items.forEach((item) => {
      item.remove();
    });
  }

  function nameContains(str, search) {
    if (str.includes(search)) {
      return true;
    }
    return false;
  }
  

  function highlightMatchingPart(name, input) {
    const lowerName = name.toLowerCase();
    const lowerInput = input.toLowerCase();
    let startIndex = lowerName.indexOf(lowerInput);

    if (startIndex !== -1) {
      let matchedPart = name.substring(startIndex, startIndex + input.length);
      return name.replace(matchedPart, `<b>${matchedPart}</b>`);
    } else {
      return name;
    }
  }

  function handleListChange(changesList, observer) {
    changesList.forEach((change) => {
      if (change.type === 'childList') {
        currentIndex = -1;
      }
    });
  }
  
}


});




