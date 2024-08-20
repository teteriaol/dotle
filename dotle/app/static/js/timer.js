const counter = {
  square: (txt) => {
    const cell = document.createElement("div");
    cell.className = `cell ${txt}`;
    cell.innerHTML = `
      <div class="digits">0</div>
      <div class="text">${txt}</div>`;
    return cell;
  },

  attach: (instance) => {
    instance.target.className = "countdown";
    if (instance.remain >= 3600) {
      instance.target.appendChild(counter.square("hours"));
      instance.hours = instance.target.querySelector(".hours .digits");
    }
    if (instance.remain >= 60) {
      instance.target.appendChild(counter.square("mins"));
      instance.mins = instance.target.querySelector(".mins .digits");
    }
    instance.target.appendChild(counter.square("secs"));
    instance.secs = instance.target.querySelector(".secs .digits");

    instance.timer = setInterval(() => counter.ticker(instance), 1000);
  },

  ticker: (instance) => {
    if (instance.remain <= 0) {
      clearInterval(instance.timer);
      instance.remain = 0;
      if (typeof instance.after === "function") {
        instance.after();
      }
      return;
    }

    instance.remain--;
    const days = Math.floor(instance.remain / 86400);
    const hours = Math.floor((instance.remain % 86400) / 3600);
    const mins = Math.floor((instance.remain % 3600) / 60);
    const secs = instance.remain % 60;

    if (instance.secs) instance.secs.textContent = secs;
    if (instance.mins) instance.mins.textContent = mins;
    if (instance.hours) instance.hours.textContent = hours;
  },

  toSecs: (till) => {
    const remain = Math.floor(till / 1000) - Math.floor(Date.now() / 1000);
    return remain < 0 ? 0 : remain;
  },
};

function fetchData() {
  $.ajax({
    url: '/api/generate_hero/',
    type: 'GET',
    success: function(response) {
      if (response.reload_needed) {
        location.reload();
      }
    },
    error: function(error) {
      console.error(error);
    }
  });
}

window.onload = () => {
  fetchData();
  const nextUTCDay = new Date();
  nextUTCDay.setUTCDate(nextUTCDay.getUTCDate() + 1);
  nextUTCDay.setUTCHours(0, 0, 0, 0);
  let remainingTime = counter.toSecs(nextUTCDay);

  const timerElement = document.getElementById("timer");
  const instance = {
    target: timerElement,
    remain: remainingTime,
    hours: null,
    mins: null,
    secs: null,
    timer: null,
    after: fetchData
  };
  
  counter.attach(instance);
};
