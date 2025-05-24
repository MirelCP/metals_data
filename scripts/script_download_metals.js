const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

// Parámetros fijos
const targetUrl = "https://www.tradingview.com/markets/futures/quotes-metals/";

// Lista de user agents realistas
const userAgents = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
  "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
];

// Accept-Language aleatorio
const acceptLanguages = [
  'en-US,en;q=0.9',
  'es-ES,es;q=0.9',
  'en;q=0.9'
];

// Carpeta donde se guardarán los HTML y screenshots (fuera de /scripts)
const dataDir = path.join(__dirname, "data");
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

const delay = (min, max) =>
  new Promise(resolve => setTimeout(resolve, Math.random() * (max - min) + min));

(async () => {
  const sessionId = crypto.randomBytes(4).toString('hex');
  const userAgent = userAgents[Math.floor(Math.random() * userAgents.length)];
  const acceptLanguage = acceptLanguages[Math.floor(Math.random() * acceptLanguages.length)];

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ],
    defaultViewport: null
  });

  const page = await browser.newPage();
  await page.setUserAgent(userAgent);
  await page.setExtraHTTPHeaders({
    'Accept-Language': acceptLanguage,
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
  });

  // Espera humana antes de navegar
  await delay(2000, 4000);

  try {
    console.log(`🌍 Navegando a: ${targetUrl}`);
    await page.goto(targetUrl, { waitUntil: "networkidle2", timeout: 40000 });
  } catch (err) {
    console.log(`⚠️ Error al cargar la página: ${err.message}`);
    await browser.close();
    return;
  }

  // Scroll humano para cargar contenidos dinámicos
  const simulateHumanScrolling = async () => {
    const steps = Math.floor(Math.random() * 5) + 3;
    for (let i = 0; i < steps; i++) {
      await page.evaluate(() => window.scrollBy(0, window.innerHeight * 0.6));
      await delay(400, 800);
    }
  };
  await simulateHumanScrolling();

  await delay(1500, 2500);

  // Guardar el HTML de la página
  const cleanUrl = targetUrl.replace(/[^a-zA-Z0-9]/g, "_").slice(0, 60);
  const filename = `download_${cleanUrl}_${sessionId}.html`;
  const filePath = path.join(dataDir, filename);

  const html = await page.content();
  fs.writeFileSync(filePath, html, "utf-8");
  console.log(`✅ Página guardada en ${filePath}`);

  // Guardar screenshot por si quieres
  const screenshotPath = path.join(dataDir, `screenshot_${cleanUrl}_${sessionId}.png`);
  await page.screenshot({ path: screenshotPath });
  console.log(`📸 Screenshot guardada en ${screenshotPath}`);

  await browser.close();
  console.log("🏁 Proceso completado.");
})();
