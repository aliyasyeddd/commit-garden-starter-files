/*PAGE NAVIGATION */
function showPage(name) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('page-' + name).classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(b => {
    if (b.getAttribute('title').toLowerCase() === name) b.classList.add('active');
  });
}


/* INIT — load page partials then garden */
async function loadGarden() {
  try {
    const res  = await fetch('/garden-data');
    const data = await res.json();
    const { streak, wilting } = data;
    const best  = data.best_streak   || 0;
    const total = data.total_commits || 0;

    // Topbar
    document.getElementById('streakTop').textContent  = '🔥' + streak + 'd';
    document.getElementById('bestTop').textContent    = best + 'd';
    document.getElementById('totalTop').textContent   = total;
    document.getElementById('statusQuote').textContent = getQuote(wilting);

    // Plant panel
    document.getElementById('streakRight').textContent = streak;
    document.getElementById('bestRight').textContent   = best;
    document.getElementById('totalRight').textContent  = total;
    document.getElementById('plantName').textContent   = getPlantEmoji(streak) + ' ' + getPlantName(streak);
    document.getElementById('stageFill').style.width   = getStagePercent(streak) + '%';
    document.getElementById('stageLabel').textContent  = getNextUnlock(streak);
    document.getElementById('plantImg').src            = '/svg?t=' + Date.now();



    // Today's date
    document.getElementById('todayDate').textContent = new Date().toLocaleDateString('en-US', {
      weekday: 'long', month: 'long', day: 'numeric'
    });

    loadRecentLogs();
    updatePlantsPage(streak);

  } catch (e) {
    document.getElementById('statusQuote').textContent = 'Could not load garden data';
  }
}

/* PLANTS PAGE */
function updatePlantsPage(streak) {
  document.getElementById('plantsSubtitle').textContent =
    `Current streak: ${streak} days — keep going to unlock more plants`;

  const unlocks = PLANT_UNLOCKS;

  unlocks.forEach(({ id, day, unlockEl }) => {
    const card    = document.getElementById('showcase-' + id);
    const badge   = card.querySelector('.plant-showcase-badge');
    const labelEl = document.getElementById(unlockEl);

    if (streak >= day) {
      card.classList.remove('locked');
      badge.classList.replace('locked-badge', 'unlocked');
      badge.textContent  = 'Unlocked';
      labelEl.textContent = `Unlocked at Day ${day} ✓`;
    } else {
      labelEl.textContent = `${day - streak} days to go`;
    }
  });

  // Show live SVG for current plant
  const currentPlant = streak >= 30 ? 'sunflower'
    : streak >= 21 ? 'blossom'
    : streak >= 11 ? 'tree'
    : streak >= 6  ? 'cactus'
    : 'sprout';


  const currentCard = document.getElementById('showcase-' + currentPlant);
  if (currentCard) {
    const imgContainer = currentCard.querySelector('.plant-showcase-img');
    imgContainer.innerHTML = `<img src="/svg?t=${Date.now()}" alt="Current plant" style="width:100px; height:120px; object-fit:contain;" />`;
  } 

  const sproutBadge = document.querySelector('#showcase-sprout .plant-showcase-badge');
  sproutBadge.textContent = streak >= 6 ? 'Completed' : 'Current';
}

/* RECENT LOGS */
async function loadRecentLogs() {
  const container = document.getElementById('recentLogs');
  try {
    const res     = await fetch('/logs');
    const entries = await res.json();

    if (!entries.length) {
      container.innerHTML = '<div class="empty-state">No logs yet. Make your first commit!</div>';
      return;
    }

    container.innerHTML = entries.slice(0, 3).map(e => `
      <div class="recent-log-item">
        <div class="recent-log-text">${e.text}</div>
        <div class="recent-log-date">${e.date}</div>
      </div>
    `).join('');
  } catch {
    container.innerHTML = '<div class="empty-state">Could not load logs</div>';
  }
}


loadGarden();