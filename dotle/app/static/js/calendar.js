document.addEventListener("DOMContentLoaded", function () {
    const statsContainer = document.querySelector('.stats__container');
    const infoContainer = document.querySelector('.question__container');
    const statsIcon = document.querySelector('.stats');
    const infoIcon = document.querySelector('.question');
    const calendarIcon = document.querySelector('.calendar__icon');
    const calendarContainer = document.querySelector('.container-calendar');
    const statsButtons = document.querySelectorAll('.stats__button')
    const statsRankedList = document.querySelector('.ranked')
    const statsClassicList = document.querySelector('.classic')
    let currentDay = window.location.href;
    let past = false;



    const buttonsComponent = document.querySelector('.menu__container');
    const buttonsToggle = document.querySelector('.menu');


    statsIcon.addEventListener('click', function(e) { 
        if (!statsContainer.classList.contains('active')) {
            let width = 0;
            statsContainer.classList.toggle('active');
            statsAnimation = setInterval(function() {
            width += 50;
            statsContainer.style.width = width + 'px';
            if (width >= 350) {
                clearInterval(statsAnimation);
            }
            statsContainer.style.padding = '15px';
            statsContainer.style.border = '10px solid rgba(0,0,0,0.5)';
            }, 1);
        } else {
            let width = 350;
            statsAnimation = setInterval(function() {
                width -= 50;
                statsContainer.style.width = width + 'px';
                if (width == 0) {
                    clearInterval(statsAnimation);
                    statsContainer.style.width = '0';
                    statsContainer.style.padding = '0';
                    statsContainer.style.border = 'none';
                    statsContainer.classList.toggle('active')
                }
            }, 1);
        }
    });
    calendarIcon.addEventListener('click', function(e) {
        if (!calendarContainer.classList.contains('active')) {
            let width = 0;
            calendarContainer.classList.toggle('active');
            statsAnimation = setInterval(function() {
            width += 50;
            calendarContainer.style.width = width + 'px';
            if (width >= 350) {
                clearInterval(statsAnimation);
            }
            calendarContainer.style.padding = '15px';
            calendarContainer.style.border = '10px solid rgba(0,0,0,0.5)';
            }, 1);
        } else {
            let width = 350;
            statsAnimation = setInterval(function() {
                width -= 50;
                calendarContainer.style.width = width + 'px';
                if (width == 0) {
                    clearInterval(statsAnimation);
                    calendarContainer.style.width = '0';
                    calendarContainer.style.padding = '0';
                    calendarContainer.style.border = 'none';
                    calendarContainer.classList.toggle('active')
                }
            }, 1);
        }
    });
    infoIcon.addEventListener('click', function(e) { 
        if (!infoContainer.classList.contains('active')) {
            let width = 0;
            infoContainer.classList.toggle('active');
            statsAnimation = setInterval(function() {
            width += 50;
            infoContainer.style.width = width + 'px';
            if (width >= 350) {
                clearInterval(statsAnimation);
            }
            infoContainer.style.padding = '15px';
            infoContainer.style.border = '10px solid rgba(0,0,0,0.5)';
            }, 1);
        } else {
            let width = 350;
            statsAnimation = setInterval(function() {
                width -= 50;
                infoContainer.style.width = width + 'px';
                if (width == 0) {
                    clearInterval(statsAnimation);
                    infoContainer.style.width = '0';
                    infoContainer.style.padding = '0';
                    infoContainer.style.border = 'none';
                    infoContainer.classList.toggle('active')
                }
            }, 1);
        }
    });
    
    buttonsToggle.addEventListener('click', toggleButtons);

    function toggleButtons() {
        buttonsToggle.classList.toggle('menu--active');
        buttonsComponent.classList.toggle('menu__container--active');
        document.activeElement.blur();
    }

    if(currentDay.includes('-')){
        past = true
        currentDay = currentDay.split('/');
        currentDay = currentDay[currentDay.length-1];
        currentDay = currentDay.split('-');
        currentDay = currentDay[2]+'.'+currentDay[1]+'.'+currentDay[0];
        document.querySelector('.day__heading').innerText = 'Guess a hero of '+currentDay;
    }

    statsButtons.forEach(item => {
        item.addEventListener('click', () => {
          if (!item.classList.contains('active')) {
            statsButtons.forEach(otherItem => {
              otherItem.classList.remove('active');
            });
                item.classList.add('active');
                if(item.innerHTML == 'Ranked') {
                    statsRankedList.style.display = 'block';
                    statsClassicList.style.display = 'none';
                } else {
                    statsClassicList.style.display = 'block'
                    statsRankedList.style.display = 'none'
                }
          }
        });
      });
});

function add_click_event(){
    var clickableCells = document.querySelectorAll(".date-picker.available");
    clickableCells.forEach(function(cell) {
        cell.addEventListener("click", function() {
            var year = cell.getAttribute("data-year");
            var month = cell.getAttribute("data-month");
            var date = cell.getAttribute("data-date");

            if (month < 10) {
              month = "0" + month;
            }
            if (date < 10) {
              date = "0" + date;
            }
            var destinationURL = "/" + window.location.pathname.split('/')[1] + "/" + year + "-" + month + "-" + date;
            // var destinationURL = "/classic/" 
            // if (date != today.getUTCDate()){
            //     destinationURL += year + "-" + month + "-" + date;
            // }
            if (window.location.pathname != destinationURL){
                window.location.href = destinationURL;
            }
        });
    });
}

function generate_year_range(start, end) {
    var years = "";
    for (var year = start; year <= end; year++) {
        years += "<option value='" + year + "'>" + year + "</option>";
    }
    return years;
}

today = new Date();
// first_generative_date = new Date('2023-09-01');
// console.log(first_generative_date);
currentMonth = today.getUTCMonth();
currentYear = today.getUTCFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");


createYear = generate_year_range(2023, 2024);
/** or
 * createYear = generate_year_range( 1970, currentYear );
 */
if(document.querySelector(".calendar__icon") != null){
document.getElementById("year").innerHTML = createYear;
}
var calendar = document.getElementById("calendar");
if(calendar!= null){
var lang = calendar.getAttribute('data-lang');
}
var months = "";
var days = "";

var monthDefault = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

var dayDefault = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

months = monthDefault;
days = dayDefault;


var $dataHead = "<tr>";
for (dhead in days) {
    $dataHead += "<th data-days='" + days[dhead] + "'>" + days[dhead] + "</th>";
}
$dataHead += "</tr>";

//alert($dataHead);
if(calendar!=null){
document.getElementById("thead-month").innerHTML = $dataHead;


monthAndYear = document.getElementById("monthAndYear");
showCalendar(currentMonth, currentYear);
}


function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

function showCalendar(month, year) {

    var firstDay = (( new Date( year, month ) ).getDay()+6) % 7;

    tbl = document.getElementById("calendar-body");

    
    tbl.innerHTML = "";

    
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;

    // creating all cells
    var date = 1;
    for ( var i = 0; i < 6; i++ ) {
        
        var row = document.createElement("tr");

        
        for ( var j = 0; j < 7; j++ ) {
            if ( i === 0 && j < firstDay ) {
                cell = document.createElement( "td" );
                cellText = document.createTextNode("");
                cell.appendChild(cellText);
                row.appendChild(cell);
            } else if (date > daysInMonth(month, year)) {
                break;
            } else {
                cell = document.createElement("td");
                cell.setAttribute("data-date", date);
                cell.setAttribute("data-month", month + 1);
                cell.setAttribute("data-year", year);
                cell.setAttribute("data-month_name", months[month]);
                cell.className = "date-picker";
                cell.innerHTML = "<span>" + date + "</span>";

                if ( date === today.getUTCDate() && year === today.getUTCFullYear() && month === today.getUTCMonth() ) {
                    cell.className = "date-picker selected";
                }
                let todayDate = new Date(today.getUTCFullYear()+'-'+(today.getUTCMonth()+1)+ '-'+today.getUTCDate())
                let cellDate = new Date(year+'-'+(month+1)+'-'+date)
                if(cellDate >= new Date('2023-09-1') && cellDate <= todayDate ) {
                    cell.classList.add('available');
                }
                row.appendChild(cell);
                date++;
            }


        }

        tbl.appendChild(row);
    }
    add_click_event();

}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getUTCDate();
}