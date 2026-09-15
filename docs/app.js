const tg = window.Telegram.WebApp;
tg.expand();
try { tg.setHeaderColor('#FFA703'); } catch(e) {}

const BRANCHES = [
  { id:'yubileniy', name:'Yubileyniy filiali', icon:'&#127979;', landmark:"Ezaz kafesi oldida, Yuridik kollej ro'parasida",
    teachers:[{name:'Miss Kamola',spec:'Kids (9-13 yosh) va Pre-IELTS',level:'B2+'},
              {name:'Miss Dilnora',spec:'0 dan Ingliz tili',level:'B2'}] },
  { id:'dubay', name:'Dubay filiali', icon:'&#127961;', landmark:'Dubay restorani yonida',
    teachers:[{name:'Ustoz',spec:'Pre-IELTS va IELTS',level:'B2+'}] },
  { id:'yashil_dunyo', name:'Yashil Dunyo filiali', icon:'&#127807;', landmark:"Kinoteatrning 2-qavati, Yashil bozor ro'parasida",
    teachers:[{name:"Chori Tursunpo'latov",spec:'0 dan Ingliz tili',level:'B2'},
              {name:'Lobar Yaxshiboyeva',spec:'Kids va Pre-IELTS',level:'B2+'}] },
  { id:'limonariya', name:'Limonariya filiali', icon:'&#127819;', landmark:'Yangi TDPU yonida',
    teachers:[{name:'Ustoz',spec:'Grammatika va Pre-IELTS',level:'B2'}] },
  { id:'avtovokzal', name:'Avtovokzal filiali', icon:'&#128652;', landmark:"Hakim at-Termiziy masjidi yonida, eski angorski stoyankasi oldida",
    teachers:[{name:"Ilhombek Safarmuro'v",spec:'0 dan Ingliz tili va Pre-IELTS',level:'B2'}] },
  { id:'sentr', name:'Sentr filiali', icon:'&#127963;', landmark:'Shahar dehqon bozori yonida',
    teachers:[{name:'Ahmadshoh Murodullayev',spec:'IELTS (barcha 4 skill)',level:'C1 | IELTS 8.5',
               extra:'Surxondaryoda IELTS 8.5 olgan eng yuqori ball sohibi'}] },
];

const COURSES = [
  {id:'grammar',name:'Grammatika \u2014 Beginner',icon:'&#128214;'},
  {id:'pre_ielts',name:'Pre-IELTS',icon:'&#128216;'},
  {id:'ielts',name:'IELTS',icon:'&#127891;'},
  {id:'cefr',name:'CEFR Guruhlari',icon:'&#127941;'},
];

const QUESTIONS = [
  {id:1,level:'A1',text:"Choose the correct form: 'She ___ a student.'",options:['am','is','are','be'],correct:1},
  {id:2,level:'A1',text:"What is the plural of 'child'?",options:['childs','childes','children','childrens'],correct:2},
  {id:3,level:'A1',text:"I ___ to school every day.",options:['go','goes','going','went'],correct:0},
  {id:4,level:'A2',text:"Yesterday I ___ a film.",options:['watch','watches','watched','watching'],correct:2},
  {id:5,level:'A2',text:"Which sentence is correct?",options:["She don't like coffee.","She doesn't likes coffee.","She doesn't like coffee.","She not like coffee."],correct:2},
  {id:6,level:'A2',text:"There ___ many books on the shelf.",options:['is','are','be','am'],correct:1},
  {id:7,level:'B1',text:"If it ___ tomorrow, we will stay at home.",options:['rain','rains','rained','will rain'],correct:1},
  {id:8,level:'B1',text:"The book ___ written by Tolstoy.",options:['is','was','were','has'],correct:1},
  {id:9,level:'B1',text:"The film was so boring that I nearly fell ___.",options:['asleep','awake','alone','apart'],correct:0},
  {id:10,level:'B2',text:"By the time she arrived, he ___ for an hour.",options:['waited','has waited','had been waiting','was waiting'],correct:2},
  {id:11,level:'B2',text:"His argument was not very ___, so nobody agreed.",options:['persuasive','pleasant','precise','possible'],correct:0},
  {id:12,level:'B2',text:"She said: 'I am tired.' She said that she ___.",options:['is tired','was tired','were tired','had been tired'],correct:1},
  {id:13,level:'C1',text:"Choose the correct meaning of 'ubiquitous':",options:['Rare and unusual','Appearing everywhere at the same time','Extremely expensive','Difficult to understand'],correct:1},
  {id:14,level:'C1',text:"Which sentence is grammatically correct?",options:['Had I known about the meeting, I would have attended it.','If I would have known, I would attend.','Had I knew about it, I attended.','I would have attend if I knew.'],correct:0},
  {id:15,level:'C1',text:"The government needs to ___ action on climate change.",options:['do','make','take','have'],correct:2},
];

// ── TAB NAVIGATION ────────────────────────────────────────────────────────────
function showTab(tab) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
  var tabEl = document.getElementById('tab-' + tab);
  if (tabEl) tabEl.classList.add('active');
  var navEl = document.getElementById('nav-' + tab);
  if (navEl) navEl.classList.add('active');
  window.scrollTo(0, 0);
}

// ── BRANCHES ─────────────────────────────────────────────────────────────────
function renderBranches() {
  var el = document.getElementById('branches-list');
  if (!el) return;
  el.innerHTML = BRANCHES.map(function(b) {
    return '<div class="branch-card">' +
      '<div class="branch-name">' + b.icon + ' ' + b.name + '</div>' +
      '<div class="branch-landmark">&#128506; ' + b.landmark + '</div>' +
      '<span class="branch-badge">&#128104; ' + b.teachers.length + ' ta ustoz</span>' +
      '</div>';
  }).join('');
}

// ── TEACHERS ─────────────────────────────────────────────────────────────────
function renderTeachers() {
  var el = document.getElementById('teachers-list');
  if (!el) return;
  var html = '';
  BRANCHES.forEach(function(b) {
    b.teachers.forEach(function(t) {
      html += '<div class="teacher-card">' +
        '<div class="teacher-name">&#128100; ' + t.name + '</div>' +
        '<div class="teacher-spec">&#128218; ' + t.spec + '</div>' +
        '<span class="teacher-level">' + t.level + '</span>' +
        '<div class="teacher-branch">' + b.icon + ' ' + b.name + '</div>' +
        (t.extra ? '<div class="teacher-extra">&#11088; ' + t.extra + '</div>' : '') +
        '</div>';
    });
  });
  el.innerHTML = html;
}

// ── QUIZ ─────────────────────────────────────────────────────────────────────
var qIdx = 0, score = 0, answered = false;

function startQuiz() {
  qIdx = 0; score = 0; answered = false;
  document.getElementById('quiz-start-screen').style.display = 'none';
  document.getElementById('quiz-result-screen').style.display = 'none';
  document.getElementById('quiz-question-screen').style.display = 'block';
  showQuestion(0);
}

function restartQuiz() {
  document.getElementById('quiz-result-screen').style.display = 'none';
  document.getElementById('quiz-start-screen').style.display = 'block';
}

function showQuestion(idx) {
  answered = false;
  var q = QUESTIONS[idx];
  var pct = Math.round(idx / 15 * 100);
  document.getElementById('quiz-fill').style.width = pct + '%';
  document.getElementById('quiz-meta').innerHTML =
    '<span>Savol ' + (idx+1) + '/15</span><span>Daraja: ' + q.level + '</span>';
  document.getElementById('quiz-question').textContent = q.text;
  var labels = ['A','B','C','D'];
  document.getElementById('quiz-options').innerHTML = q.options.map(function(opt, i) {
    return '<button class="quiz-opt" onclick="selectAnswer(' + idx + ',' + i + ',this)">' +
      '<span class="opt-label">' + labels[i] + '</span> ' + opt + '</button>';
  }).join('');
}

function selectAnswer(qi, chosen, btn) {
  if (answered) return;
  answered = true;
  var q = QUESTIONS[qi];
  var opts = document.querySelectorAll('.quiz-opt');
  opts.forEach(function(b, i) {
    if (i === q.correct) b.classList.add('correct');
    else if (i === chosen && chosen !== q.correct) b.classList.add('wrong');
    b.style.pointerEvents = 'none';
  });
  if (chosen === q.correct) score++;
  setTimeout(function() {
    if (qi < 14) showQuestion(qi + 1);
    else showResult();
  }, 700);
}

function showResult() {
  document.getElementById('quiz-question-screen').style.display = 'none';
  document.getElementById('quiz-fill').style.width = '100%';
  var r = getLevel(score);
  document.getElementById('result-emoji').textContent = r.emoji;
  document.getElementById('result-score').textContent = score + '/15';
  document.getElementById('result-level').textContent = r.level;
  document.getElementById('result-comment').textContent = r.comment;
  document.getElementById('quiz-result-screen').style.display = 'block';
  window._quizScore = score;
  window._quizLevel = r.level;
}

function getLevel(s) {
  if (s <= 3)  return {level:'A1 - Beginner', emoji:'&#127793;', comment:"Siz ingliz tilini 0 dan boshlaysiz. 4-6 oy ichida kuchli baza yaratasiz!"};
  if (s <= 6)  return {level:'A2 - Elementary', emoji:'&#128215;', comment:"Asosiy bilimingiz bor. Grammatika kursini tugatib Pre-IELTS ga o'tasiz!"};
  if (s <= 9)  return {level:'B1 - Intermediate', emoji:'&#128216;', comment:"Yaxshi daraja! Pre-IELTS kursi bilan 3-4 oyda IELTS ga tayyorlanasiz."};
  if (s <= 12) return {level:'B2 - Upper-Intermediate', emoji:'&#128217;', comment:"Zo'r natija! Bevosita IELTS kursiga o'ting. 6.5-7.5 ball realistik maqsad!"};
  return {level:'C1 - Advanced', emoji:'&#127942;', comment:"Ajoyib! IELTS 7.5-8.5 maqsad qo'yishingiz mumkin!"};
}

// ── REGISTER ─────────────────────────────────────────────────────────────────
var regData = {name:'', phone:'', branch:'', course:'', time:''};

function renderRegOptions() {
  var rb = document.getElementById('reg-branches');
  if (rb) rb.innerHTML = BRANCHES.map(function(b) {
    return '<button class="reg-option" onclick="regSelectBranch(\'' + b.id + '\',\'' + b.name + '\')">' + b.icon + ' ' + b.name + '</button>';
  }).join('');
  var rc = document.getElementById('reg-courses');
  if (rc) rc.innerHTML = COURSES.map(function(c) {
    return '<button class="reg-option" onclick="regSelectCourse(\'' + c.id + '\',\'' + c.name + '\')">' + c.icon + ' ' + c.name + '</button>';
  }).join('');
}

function updateStepDots(step) {
  for (var i = 1; i <= 5; i++) {
    var dot = document.getElementById('step-dot-' + i);
    if (!dot) continue;
    dot.classList.remove('active','done');
    if (i < step) dot.classList.add('done');
    else if (i === step) dot.classList.add('active');
  }
}

function regNext(step) {
  if (step === 1) {
    var name = document.getElementById('reg-name').value.trim();
    if (!name) { alert("Ismingizni kiriting!"); return; }
    regData.name = name;
    document.getElementById('reg-step-1').style.display = 'none';
    document.getElementById('reg-step-2').style.display = 'block';
    updateStepDots(2);
  } else if (step === 2) {
    var phone = document.getElementById('reg-phone').value.trim();
    if (!phone) { alert("Telefon raqamingizni kiriting!"); return; }
    regData.phone = phone;
    document.getElementById('reg-step-2').style.display = 'none';
    document.getElementById('reg-step-3').style.display = 'block';
    updateStepDots(3);
  }
}

function regBack(step) {
  document.getElementById('reg-step-' + step).style.display = 'none';
  document.getElementById('reg-step-' + (step-1)).style.display = 'block';
  updateStepDots(step - 1);
}

function regSelectBranch(id, name) {
  regData.branch = name;
  document.getElementById('reg-step-3').style.display = 'none';
  document.getElementById('reg-step-4').style.display = 'block';
  updateStepDots(4);
}

function regSelectCourse(id, name) {
  regData.course = name;
  document.getElementById('reg-step-4').style.display = 'none';
  document.getElementById('reg-step-5').style.display = 'block';
  updateStepDots(5);
}

function regSelectTime(time) {
  regData.time = time;
  submitReg();
}

function submitReg() {
  var payload = JSON.stringify({
    type: 'registration',
    name: regData.name,
    phone: regData.phone,
    branch: regData.branch,
    course: regData.course,
    time_pref: regData.time,
    quiz_score: window._quizScore || null,
    quiz_level: window._quizLevel || null
  });
  try { tg.sendData(payload); } catch(e) { console.log('sendData error:', e); }
  document.getElementById('reg-step-5').style.display = 'none';
  document.getElementById('reg-success').style.display = 'block';
}

// ── INIT ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  renderBranches();
  renderTeachers();
  renderRegOptions();
  startCountdown();
  if (tg.BackButton) {
    tg.BackButton.onClick(function() { showTab('home'); });
  }
});

// Countdown — ends midnight tonight
function startCountdown() {
  function tick() {
    var now   = new Date();
    var end   = new Date(now); end.setHours(23,59,59,0);
    var diff  = Math.max(0, Math.floor((end - now) / 1000));
    var h = Math.floor(diff / 3600);
    var m = Math.floor((diff % 3600) / 60);
    var s = diff % 60;
    var pad = function(n){ return n < 10 ? '0'+n : n; };
    var eh = document.getElementById('cd-h');
    var em = document.getElementById('cd-m');
    var es = document.getElementById('cd-s');
    if (eh) eh.textContent = pad(h);
    if (em) em.textContent = pad(m);
    if (es) es.textContent = pad(s);
  }
  tick();
  setInterval(tick, 1000);
}
