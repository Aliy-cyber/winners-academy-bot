const tg = window.Telegram.WebApp;
tg.expand();
try { tg.setHeaderColor('#FFA703'); } catch(e){}

// ── DATA ─────────────────────────────────────────────────────────
const BRANCHES = [
  {id:'yubileniy', name:'Yubileyniy filiali',   icon:'&#127979;', land:"Ezaz kafesi oldida, Yuridik kollej ro'parasida",
   teachers:[{name:'Miss Kamola',spec:'Kids (9-13 yosh) va Pre-IELTS',lv:'B2+'},
             {name:'Miss Dilnora',spec:'0 dan Ingliz tili',lv:'B2'}]},
  {id:'dubay',     name:'Dubay filiali',         icon:'&#127961;', land:'Dubay restorani yonida',
   teachers:[{name:'Ustoz',spec:'Pre-IELTS va IELTS',lv:'B2+'}]},
  {id:'yashil',    name:'Yashil Dunyo filiali',  icon:'&#127807;', land:"Kinoteatrning 2-qavati, Yashil bozor ro'parasida",
   teachers:[{name:"Chori Tursunpo'latov",spec:'0 dan Ingliz tili',lv:'B2'},
             {name:'Lobar Yaxshiboyeva',spec:'Kids va Pre-IELTS',lv:'B2+'}]},
  {id:'limon',     name:'Limonariya filiali',    icon:'&#127819;', land:'Yangi TDPU yonida',
   teachers:[{name:'Ustoz',spec:'Grammatika va Pre-IELTS',lv:'B2'}]},
  {id:'avto',      name:'Avtovokzal filiali',    icon:'&#128652;', land:"Hakim at-Termiziy masjidi yonida, eski angorski stoyankasi oldida",
   teachers:[{name:"Ilhombek Safarmuro'v",spec:'0 dan Ingliz tili va Pre-IELTS',lv:'B2'}]},
  {id:'sentr',     name:'Sentr filiali',         icon:'&#127963;', land:'Shahar dehqon bozori yonida',
   teachers:[{name:'Ahmadshoh Murodullayev',spec:'IELTS (barcha 4 skill)',lv:'C1 | IELTS 8.5',
              ex:'Surxondaryoda IELTS 8.5 olgan eng yuqori ball sohibi'}]},
];

const COURSES = [
  {id:'grammar',   name:'Grammatika &mdash; Beginner', ico:'&#128214;', for:'0 dan boshlovchilar',  dur:'4&ndash;6 oy'},
  {id:'pre_ielts', name:'Pre-IELTS',                   ico:'&#128216;', for:'A2&ndash;B1 daraja',   dur:'3&ndash;5 oy'},
  {id:'ielts',     name:'IELTS',                       ico:'&#127891;', for:'B1+ daraja',           dur:'3&ndash;6 oy'},
  {id:'cefr',      name:'CEFR Guruhlari',              ico:'&#127941;', for:'B2/C1 sertifikat',     dur:'2&ndash;4 oy'},
];

const QS = [
  {lv:'A1',q:"Choose the correct form: 'She ___ a student.'",opts:['am','is','are','be'],ok:1},
  {lv:'A1',q:"What is the plural of 'child'?",opts:['childs','childes','children','childrens'],ok:2},
  {lv:'A1',q:"I ___ to school every day.",opts:['go','goes','going','went'],ok:0},
  {lv:'A2',q:"Yesterday I ___ a film.",opts:['watch','watches','watched','watching'],ok:2},
  {lv:'A2',q:"Which sentence is correct?",opts:["She don't like coffee.","She doesn't likes coffee.","She doesn't like coffee.","She not like coffee."],ok:2},
  {lv:'A2',q:"There ___ many books on the shelf.",opts:['is','are','be','am'],ok:1},
  {lv:'B1',q:"If it ___ tomorrow, we will stay at home.",opts:['rain','rains','rained','will rain'],ok:1},
  {lv:'B1',q:"The book ___ written by Tolstoy.",opts:['is','was','were','has'],ok:1},
  {lv:'B1',q:"The film was so boring that I nearly fell ___.",opts:['asleep','awake','alone','apart'],ok:0},
  {lv:'B2',q:"By the time she arrived, he ___ for an hour.",opts:['waited','has waited','had been waiting','was waiting'],ok:2},
  {lv:'B2',q:"His argument was not very ___, so nobody agreed.",opts:['persuasive','pleasant','precise','possible'],ok:0},
  {lv:'B2',q:"She said: 'I am tired.' She said that she ___.",opts:['is tired','was tired','were tired','had been tired'],ok:1},
  {lv:'C1',q:"Choose the correct meaning of 'ubiquitous':",opts:['Rare and unusual','Appearing everywhere at the same time','Extremely expensive','Difficult to understand'],ok:1},
  {lv:'C1',q:"Which sentence is grammatically correct?",opts:['Had I known, I would have attended.','If I would have known, I would attend.','Had I knew, I attended.','I would have attend if I knew.'],ok:0},
  {lv:'C1',q:"The government needs to ___ action on climate change.",opts:['do','make','take','have'],ok:2},
];

// ── TABS ─────────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab').forEach(function(t){ t.classList.remove('active'); });
  document.querySelectorAll('.nb').forEach(function(b){ b.classList.remove('active'); });
  var t = document.getElementById('tab-'+name);
  var b = document.getElementById('nav-'+name);
  if(t) t.classList.add('active');
  if(b) b.classList.add('active');
  window.scrollTo(0,0);
}

// ── COURSES ──────────────────────────────────────────────────────
function renderCourses() {
  var el = document.getElementById('courses-list');
  if(!el) return;
  el.innerHTML = COURSES.map(function(c){
    return '<div class="c-card" onclick="showTab(\'register\')">' +
      '<span class="c-ico">'+c.ico+'</span>' +
      '<div><b>'+c.name+'</b><p>'+c.for+' &bull; '+c.dur+'</p></div>' +
      '<span class="c-arr">&#8250;</span></div>';
  }).join('');
}

// ── BRANCHES ─────────────────────────────────────────────────────
function renderBranches() {
  var el = document.getElementById('branches-list');
  if(!el) return;
  el.innerHTML = BRANCHES.map(function(b){
    return '<div class="br-card">' +
      '<div class="br-name">'+b.icon+' '+b.name+'</div>' +
      '<div class="br-land">&#128506; '+b.land+'</div>' +
      '<span class="br-badge">&#128100; '+b.teachers.length+' ta ustoz</span>' +
      '</div>';
  }).join('');
}

// ── TEACHERS ─────────────────────────────────────────────────────
function renderTeachers() {
  var el = document.getElementById('teachers-list');
  if(!el) return;
  var h='';
  BRANCHES.forEach(function(b){
    b.teachers.forEach(function(t){
      h += '<div class="tc-card">' +
        '<div class="tc-name">&#128100; '+t.name+'</div>' +
        '<div class="tc-spec">&#128218; '+t.spec+'</div>' +
        '<span class="tc-lv">'+t.lv+'</span>' +
        '<div class="tc-br">'+b.icon+' '+b.name+'</div>' +
        (t.ex ? '<div class="tc-ex">&#11088; '+t.ex+'</div>' : '') +
        '</div>';
    });
  });
  el.innerHTML = h;
}

// ── QUIZ ─────────────────────────────────────────────────────────
var qi=0, sc=0, ans=false;

function startQuiz() {
  qi=0; sc=0; ans=false;
  document.getElementById('q-intro').style.display='none';
  document.getElementById('q-result').style.display='none';
  document.getElementById('q-screen').style.display='block';
  showQ(0);
}
function restartQuiz() {
  document.getElementById('q-result').style.display='none';
  document.getElementById('q-intro').style.display='block';
}
function showQ(i) {
  ans=false;
  var q=QS[i];
  var pct=Math.round(i/15*100);
  document.getElementById('qfill').style.width=pct+'%';
  document.getElementById('qmeta').innerHTML='<span>Savol '+(i+1)+'/15</span><span>'+q.lv+'</span>';
  document.getElementById('qtext').textContent=q.q;
  var L=['A','B','C','D'];
  document.getElementById('qopts').innerHTML=q.opts.map(function(o,j){
    return '<button class="q-opt" onclick="pickA('+i+','+j+',this)"><span class="opt-lb">'+L[j]+'</span>'+o+'</button>';
  }).join('');
}
function pickA(i,ch,btn) {
  if(ans) return; ans=true;
  var q=QS[i];
  document.querySelectorAll('.q-opt').forEach(function(b,j){
    if(j===q.ok) b.classList.add('ok');
    else if(j===ch&&ch!==q.ok) b.classList.add('no');
    b.style.pointerEvents='none';
  });
  if(ch===q.ok) sc++;
  setTimeout(function(){ i<14 ? showQ(i+1) : showResult(); }, 650);
}
function showResult() {
  document.getElementById('q-screen').style.display='none';
  document.getElementById('qfill').style.width='100%';
  var r=lvl(sc);
  document.getElementById('rem').textContent=r.em;
  document.getElementById('rsc').textContent=sc+'/15';
  document.getElementById('rlv').textContent=r.lv;
  document.getElementById('rcm').textContent=r.cm;
  document.getElementById('q-result').style.display='block';
  window._qsc=sc; window._qlv=r.lv;
}
function lvl(s) {
  if(s<=3)  return {lv:'A1 - Beginner',           em:'&#127793;', cm:"Siz ingliz tilini 0 dan boshlaysiz. 4-6 oy ichida kuchli baza yaratasiz!"};
  if(s<=6)  return {lv:'A2 - Elementary',          em:'&#128215;', cm:"Asosiy bilimingiz bor. Grammatika kursini tugatib Pre-IELTS ga o'tasiz!"};
  if(s<=9)  return {lv:'B1 - Intermediate',        em:'&#128216;', cm:"Yaxshi daraja! Pre-IELTS kursi bilan 3-4 oyda IELTS ga tayyorlanasiz."};
  if(s<=12) return {lv:'B2 - Upper-Intermediate',  em:'&#128217;', cm:"Zo'r natija! Bevosita IELTS ga o'ting. 6.5-7.5 ball maqsad!"};
  return              {lv:'C1 - Advanced',          em:'&#127942;', cm:"Ajoyib! IELTS 7.5-8.5 maqsad qo'yishingiz mumkin!"};
}

// ── REGISTER ─────────────────────────────────────────────────────
var RD={name:'',phone:'',branch:'',course:'',time:''};

function renderRegOpts() {
  var rb=document.getElementById('rg-br');
  if(rb) rb.innerHTML=BRANCHES.map(function(b){
    return '<button class="rg-opt" onclick="rgBr(\''+b.id+'\',\''+b.name+'\')">'+b.icon+' '+b.name+'</button>';
  }).join('');
  var rc=document.getElementById('rg-co');
  if(rc) rc.innerHTML=COURSES.map(function(c){
    return '<button class="rg-opt" onclick="rgCo(\''+c.id+'\',\''+c.name+'\')">'+c.ico+' '+c.name+'</button>';
  }).join('');
}

function updDots(s) {
  for(var i=1;i<=5;i++){
    var d=document.getElementById('d'+i);
    if(!d) continue;
    d.classList.remove('active','done');
    if(i<s) d.classList.add('done');
    else if(i===s) d.classList.add('active');
  }
}

function rgNext(s) {
  if(s===1){
    var v=document.getElementById('rg-name').value.trim();
    if(!v){alert("Ismingizni kiriting!");return;}
    RD.name=v;
    document.getElementById('rg1').style.display='none';
    document.getElementById('rg2').style.display='block';
    updDots(2);
  } else if(s===2){
    var v=document.getElementById('rg-phone').value.trim();
    if(!v){alert("Telefon raqamingizni kiriting!");return;}
    RD.phone=v;
    document.getElementById('rg2').style.display='none';
    document.getElementById('rg3').style.display='block';
    updDots(3);
  }
}
function rgBack(s) {
  document.getElementById('rg'+s).style.display='none';
  document.getElementById('rg'+(s-1)).style.display='block';
  updDots(s-1);
}
function rgBr(id,name){ RD.branch=name; document.getElementById('rg3').style.display='none'; document.getElementById('rg4').style.display='block'; updDots(4); }
function rgCo(id,name){ RD.course=name; document.getElementById('rg4').style.display='none'; document.getElementById('rg5').style.display='block'; updDots(5); }
function rgTime(t){ RD.time=t; submitReg(); }

function submitReg() {
  var p=JSON.stringify({type:'registration',name:RD.name,phone:RD.phone,
    branch:RD.branch,course:RD.course,time_pref:RD.time,
    quiz_score:window._qsc||null,quiz_level:window._qlv||null});
  try{tg.sendData(p);}catch(e){console.log(e);}
  document.getElementById('rg5').style.display='none';
  document.getElementById('rg-ok').style.display='block';
  updDots(6);
}

// ── INIT ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function(){
  renderCourses();
  renderBranches();
  renderTeachers();
  renderRegOpts();
  if(tg.BackButton){ tg.BackButton.onClick(function(){ showTab('home'); }); }
});
