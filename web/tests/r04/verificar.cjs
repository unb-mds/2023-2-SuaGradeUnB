// API controlada, idêntica nas variantes. Não mede o site público nem desempenho.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { execFileSync } = require('node:child_process');
const massa = require('./massa.json');
const baseURL = process.env.BASE_URL || 'http://127.0.0.1:3046';
const variant = process.env.VARIANTE;
assert(['antes', 'depois'].includes(variant), 'Defina VARIANTE=antes ou depois');
assert(process.env.FONTE, 'Defina FONTE com o checkout testado');
const out = path.resolve(process.env.EVIDENCIAS || '../../docs/avaliacao/dados/acao-r04', variant);
fs.mkdirSync(out, { recursive: true });
const KEY = 'suagrade:selected-classes:v1';
const results = [];
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  const browser = await chromium.launch({ headless: true });
  const metadata = {
    startedAt: new Date().toISOString(), variant, baseURL,
    sourceCommit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: process.env.FONTE }).toString().trim(),
    sourceStatus: execFileSync('git', ['status', '--short'], { cwd: process.env.FONTE }).toString(),
    node: process.version, playwright: require('playwright/package.json').version,
    browser: browser.version(), os: `${os.platform()} ${os.release()} ${os.arch()}`,
    api: 'Interceptada pelo Playwright; massa.json sintética; sem banco, login real ou SIGAA',
    devices: { computador: { width: 1366, height: 900 }, celular: { width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 3 } },
  };
  try {
    for (const [device, options] of Object.entries(metadata.devices)) {
      const context = await browser.newContext(device === 'computador' ? { viewport: options } : { ...options, viewport: { width: options.width, height: options.height } });
      const page = await context.newPage();
      let periods = [...massa.periods];
      let courses = structuredClone(massa.disciplines);
      let delay = 0, failCourses = false, authenticated = false;
      const pageErrors = [];
      page.on('pageerror', error => pageErrors.push(error.message));
      await page.route('**/*', async route => {
        const url = new URL(route.request().url());
        if (url.pathname === '/courses/year-period/') {
          return route.fulfill({ json: { 'year/period': periods } });
        }
        if (url.pathname === '/courses/') {
          if (delay) await sleep(delay);
          return route.fulfill(failCourses ? { status: 503, json: { detail: 'Indisponível no teste' } } : { json: courses });
        }
        if (url.pathname === '/users/login/') return route.fulfill(authenticated
          ? { json: { access: 'token-sintetico', first_name: 'Teste R04', email: 'teste@example.invalid' } }
          : { status: 401, json: {} });
        if (url.pathname === '/courses/schedules/') return route.fulfill({ json: [] });
        if (url.pathname === '/users/logout/') return route.fulfill({ json: {} });
        return route.continue();
      });
      const count = () => page.locator('img[alt="deletar"]').count();
      const waitCount = async expected => {
        await page.waitForFunction(n => document.querySelectorAll('img[alt="deletar"]').length === n, expected);
      };
      const home = async () => {
        await page.goto(`${baseURL}/schedules/home`);
        await page.getByRole('button', { name: 'Buscar matéria', exact: true }).waitFor();
        await page.getByRole('button', { name: 'Gerar Grade', exact: true }).waitFor();
      };
      const search = async () => {
        const selectedBeforeSearch = await count();
        await page.getByRole('button', { name: 'Buscar matéria', exact: true }).click();
        const select = page.locator('select').first();
        await select.selectOption('2026/2');
        await page.getByPlaceholder('Matéria ou Professor...').fill('MAT0107');
        await page.getByRole('button').filter({ has: page.locator('img[alt="ícone de pesquisa"]') }).click();
        await page.getByRole('button', { name: /ÁLGEBRA 3/ }).click();
        await page.waitForFunction(n => document.querySelectorAll('img[alt="ícone remover matéria"]').length === n, selectedBeforeSearch);
      };
      const closeSearch = () => page.getByRole('button', { name: 'Buscar matéria', exact: true }).click();
      const add = () => page.locator('img[alt="ícone adicionar matéria"]').first().click();
      const read = () => page.evaluate(key => sessionStorage.getItem(key), KEY);
      const seed = async value => {
        await page.evaluate(({ key, value }) => sessionStorage.setItem(key, value), { key: KEY, value });
        await home();
      };
      const record = (scenario, observed) => {
        results.push({ device, scenario, status: 'passou', observed, at: new Date().toISOString() });
        console.log(`${variant} | ${device} | ${scenario} | passou | ${observed}`);
      };

      await home();
      await search();
      await add();
      await closeSearch();
      await waitCount(1);
      await page.screenshot({ path: path.join(out, `${device}-R04-selecionada.png`), animations: 'disabled', scale: 'css' });
      let dialogs = 0;
      page.on('dialog', async dialog => { dialogs++; await dialog.accept(); });
      await home();
      if (variant === 'antes') {
        await waitCount(0);
        await page.getByText('Nenhuma disciplina escolhida no momento', { exact: true }).waitFor();
        assert.equal(dialogs, 0);
        record('R04', 'Seleção perdida após recarga, sem diálogo');
      } else {
        await waitCount(1);
        assert.equal(await count(), 1);
        record('R04', 'Mesma turma restaurada após recarga');
      }
      await page.screenshot({ path: path.join(out, `${device}-R04-recarregada.png`), animations: 'disabled', scale: 'css' });
      if (variant === 'depois') {
        const draft = await read();
        assert(draft);
        await home();
        await waitCount(1);
        record('segunda-recarga', 'Rascunho não sobrescrito pelo estado inicial vazio');

        await search();
        await add(); // segunda turma; a primeira já está marcada
        await closeSearch();
        await waitCount(2);
        await page.locator('img[alt="deletar"]').first().click();
        await home();
        await waitCount(1);
        assert((await page.locator('main').innerText()).includes('Sala R04-B'));
        record('remocao', 'Só a segunda turma permanece após recarga');
        await page.locator('img[alt="deletar"]').click();
        assert.equal(await read(), null);
        await home();
        await waitCount(0);
        record('limpeza', 'Remover a última turma apaga o rascunho');

        await search();
        await add();
        await page.locator('select').first().selectOption('2026/1');
        await page.getByText('Há disciplinas selecionadas de outro período, não pode haver mistura!').waitFor();
        assert.equal(await page.locator('select').first().inputValue(), '2026/2');
        await page.locator('img[alt="ícone remover matéria"]').click();
        await page.locator('select').first().selectOption('2026/1');
        assert.equal(await read(), null);
        await closeSearch();
        await home();
        await waitCount(0);
        record('troca-periodo', 'Troca com seleção bloqueada; após limpar, outro período não ressuscita rascunho');

        periods = ['2026/1'];
        await seed(draft);
        await page.waitForFunction(key => sessionStorage.getItem(key) === null, KEY);
        await waitCount(0);
        record('periodo-indisponivel', 'Rascunho de período ausente da API descartado');
        periods = [...massa.periods];
        for (const bad of ['{', 'null', '{"version":99}', JSON.stringify({ version: 1, yearPeriod: '2026/2', disciplines: [{ id: 107, code: 'MAT0107', classIds: ['10701'] }] })]) {
          await seed(bad);
          await page.waitForFunction(key => sessionStorage.getItem(key) === null, KEY);
          await waitCount(0);
        }
        record('dados-invalidos', 'JSON truncado, null, versão incompatível e ID com tipo errado ignorados');

        courses[0].classes[0].classroom = 'Sala atualizada na API';
        await seed(draft);
        await waitCount(1);
        assert((await page.locator('main').innerText()).includes('Sala atualizada na API'));
        record('dados-atuais', 'Dados exibidos vêm da API, sem confiar no rascunho');
        courses[0].classes = [];
        await seed(draft);
        await page.waitForFunction(key => sessionStorage.getItem(key) === null, KEY);
        await waitCount(0);
        record('turma-obsoleta', 'Turma que deixou de existir não restaurada');

        courses = structuredClone(massa.disciplines);
        failCourses = true;
        await seed(draft);
        await page.getByText(/Não foi possível recuperar/).waitFor();
        assert.equal(await read(), draft);
        record('api-indisponivel', 'Rascunho mantido para tentar novamente após recarga');
        failCourses = false;
        await home();
        await waitCount(1);

        delay = 1200;
        await home();
        await page.getByRole('button', { name: 'Buscar matéria', exact: true }).click();
        await page.locator('select').first().selectOption('2026/1');
        await sleep(1400);
        assert.equal(await read(), null);
        await closeSearch();
        await waitCount(0);
        record('restauracao-concorrente', 'Resposta atrasada não sobrescreve alteração feita durante restauração');
        delay = 0;

        await seed(draft);
        await waitCount(1);
        // Aba independente: sem opener, deve começar sem rascunho.
        const other = await context.newPage();
        await other.goto(`${baseURL}/schedules/home`);
        assert.equal(await other.evaluate(key => sessionStorage.getItem(key), KEY), null);
        await other.close();
        record('outra-aba', 'SessionStorage isolado em uma nova aba independente');

        authenticated = true;
        await home();
        await waitCount(1);
        await search();
        await add();
        await closeSearch();
        await waitCount(2);
        await page.locator('button[name="profile"]').click();
        await page.getByRole('button', { name: 'Sair', exact: true }).click();
        await page.waitForURL(baseURL + '/');
        assert.equal(await read(), null);
        authenticated = false;
        await home();
        await waitCount(0);
        record('limpar-toda-selecao', 'Sair executa setSelectedClasses(new Map()) e remove todo o rascunho');

        await seed(draft);
        await waitCount(1);

        await page.evaluate(key => {
          const originalGet = Storage.prototype.getItem;
          Storage.prototype.getItem = function (name) {
            if (name === key) throw new DOMException('Bloqueado no teste', 'SecurityError');
            return originalGet.call(this, name);
          };
          Storage.prototype.setItem = function () { throw new DOMException('Bloqueado no teste', 'QuotaExceededError'); };
          Storage.prototype.removeItem = function () { throw new DOMException('Bloqueado no teste', 'SecurityError'); };
        }, KEY);
        await page.locator('img[alt="deletar"]').click();
        await waitCount(0);
        await search();
        await add();
        await closeSearch();
        await waitCount(1);
        record('storage-indisponivel', 'Falhas de escrita e remoção não interrompem a seleção em memória');
      }
      assert.deepEqual(pageErrors, []);
      record('erros-javascript', 'Nenhum pageerror observado');
      await context.close();
    }
  } finally {
    metadata.finishedAt = new Date().toISOString();
    fs.writeFileSync(path.join(out, 'metadados.json'), JSON.stringify(metadata, null, 2) + '\n');
    fs.writeFileSync(path.join(out, 'resultados.json'), JSON.stringify(results, null, 2) + '\n');
    await browser.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
