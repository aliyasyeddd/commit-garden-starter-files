/* QUOTE HELPER */
function getQuote(wilting) {
  const list = wilting ? QUOTES.wilting : QUOTES.healthy;
  return list[Math.floor(Math.random() * list.length)];
}

/* PLANT HELPERS */
function getPlantName(streak) {
  if (streak >= 30) return 'Sunflower';
  if (streak >= 21) return 'Cherry Blossom';
  if (streak >= 11) return 'Tree';
  if (streak >= 6)  return 'Cactus';
  return 'Sprout';
}

function getPlantEmoji(streak) {
  if (streak >= 30) return '🌻';
  if (streak >= 21) return '🌸';
  if (streak >= 11) return '🌳';
  if (streak >= 6)  return '🌵';
  return '🌱';
}


function getStagePercent(streak) {
  if (streak >= 30) return 100;
  if (streak >= 21) return ((streak - 21) / 9) * 100;
  if (streak >= 11) return ((streak - 11) / 10) * 100;
  if (streak >= 6)  return ((streak - 6) / 5) * 100;
  return (streak / 6) * 100;
}

function getNextUnlock(streak) {
  if (streak >= 30) return "Max stage reached! You're a legend. 🌻";
  if (streak >= 21) return `Sunflower unlocks at day 30 — ${30 - streak} days to go`;
  if (streak >= 11) return `Cherry Blossom unlocks at day 21 — ${21 - streak} days to go`;
  if (streak >= 6)  return `Tree unlocks at day 11 — ${11 - streak} days to go`;
  return `Cactus unlocks at day 6 — ${6 - streak} days to go`;
}