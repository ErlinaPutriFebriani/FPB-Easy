// Test public/js/fpb.js dengan kasus yang SAMA seperti tests/test_fpb.py.
// Jalankan (Node.js 22+):  node tests/fpb.test.mjs
import { readFileSync } from 'node:fs';
import { strict as assert } from 'node:assert';
import * as fpbJs from '../public/js/fpb.js';

const kasus = JSON.parse(readFileSync(new URL('./kasus_fpb.json', import.meta.url), 'utf8'));
let lulus = 0;

function uji(nama, fn) {
  try {
    fn();
    lulus++;
  } catch (err) {
    console.error(`GAGAL: ${nama}\n  ${err.message}`);
    process.exitCode = 1;
  }
}

for (const k of kasus.faktor) {
  uji(`faktor(${k.n})`, () => assert.deepEqual(fpbJs.faktor(k.n), k.faktor));
}
for (const k of kasus.fpb) {
  uji(`fpb(${k.bilangan})`, () => {
    assert.equal(fpbJs.fpb(...k.bilangan), k.fpb);
    assert.deepEqual(fpbJs.faktorPersekutuan(...k.bilangan), k.persekutuan);
  });
}
for (const salah of kasus.tidak_valid) {
  uji(`validasi menolak ${JSON.stringify(salah)}`, () => assert.throws(() => fpbJs.validasi(salah)));
}
uji('teksPasangan(16)', () => assert.equal(fpbJs.teksPasangan(16), '16 = 1×16 = 2×8 = 4×4'));
uji('langkahFPB(20, 28)', () => {
  const l = fpbJs.langkahFPB(20, 28);
  assert.deepEqual(l.map((x) => x.judul), ['Faktor 20', 'Faktor 28', 'Faktor persekutuan', 'FPB']);
  assert.deepEqual(l[3].isi, [4]);
});
uji('hitung(["18","27"])', () => {
  const h = fpbJs.hitung(['18', '27']);
  assert.equal(h.fpb, 9);
  assert.deepEqual(h.faktor_persekutuan, [1, 3, 9]);
});

console.log(`${lulus} test lulus${process.exitCode ? ', ada yang GAGAL' : ''}.`);
