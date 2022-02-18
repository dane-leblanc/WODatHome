"use strict";
const $container = $(".container-workout");
const BASE_URL = "http://127.0.0.1:5000";
const $selectedList = $("#selected-exercises");
const $clearBtn = $("#clear-button");
const $saveBtn = $("#save-rft");
let excList = [];
let $rounds = +$("#rounds").val();

if (localStorage.rounds) {
  $("#rounds").val(+localStorage.rounds);
  $rounds = +localStorage.rounds;
}

if (localStorage.excList) {
  for (let ex of JSON.parse(localStorage.excList)) {
    excList.push(ex);
  }
  fillExercises();
}

$container.on("click", ".btn-success", function (e) {
  let exerciseId = +$(e.target).attr("data-id");
  let exerciseName = $(e.target).attr("data-name");
  let newExc = {
    id: exerciseId,
    name: exerciseName,
  };
  excList.push(newExc);
  localStorage.setItem("excList", JSON.stringify(excList));
  addExercise(newExc);
});

$container.on("dblclick", ".li-exercise", function (e) {
  let excId = +$(e.target).attr("data-id");
  for (let ex of excList) {
    if (ex.id === excId) {
      let index = excList.indexOf(ex);
      excList.splice(index, 1);
      localStorage.setItem("excList", JSON.stringify(excList));
      $(e.target).remove();
      return;
    }
  }
});

$clearBtn.on("click", function () {
  localStorage.clear();
  location.reload();
});
$("nav").on("click", "a", function () {
  localStorage.clear();
});

$saveBtn.on("click", async function () {
  let type = "RFT";
  let name = $("#workout-name").text();
  let username = $("#workout-name").attr("data-user");
  let stages = $rounds;
  let stage_time = 0;

  //Store workout in db.
  const workoutRes = await axios({
    url: `${BASE_URL}/api/workouts`,
    method: "POST",
    data: {
      username,
      type,
      name,
      stages,
      stage_time,
    },
  });

  //Add workout exercises to db.
  for (let i = 0; i < excList.length; i++) {
    let order = i + 1;
    let exercise_id = excList[i].id;
    let count = $(`input[data-exc=${exercise_id}]`).val();
    let count_type = $(`select[data-exc=${exercise_id}]`).val();
    const WorkoutExcRes = await axios({
      url: `${BASE_URL}/api/workout-exercises`,
      method: "POST",
      data: {
        name,
        order,
        exercise_id,
        count,
        count_type,
      },
    });
  }
  localStorage.clear();
  window.location.href = `${BASE_URL}/`;
});

function addExercise(exc) {
  let $newLi = $(
    `<li class = "li-exercise form-inline list-group-item" data-id = ${exc.id}> ${exc.name}</li>`
  );
  $selectedList.append($newLi);
  // $newLi.appendTo($selectedList);
  let $count = $(
    `<input type="number" class="exc-list-count form-control-sm ml-1 mr-1" data-exc="${exc.id}" value="10"/>`
  );
  $count.appendTo($newLi);
  let $countType = $(
    `<select class="exc-list-select form-control-sm" data-exc="${exc.id}">
      <option value="reps">reps</option>
      <option value="seconds">seconds</option>
    </select>`
  );
  $countType.appendTo($newLi);
}

function fillExercises() {
  for (let exc of excList) {
    addExercise(exc);
  }
}
