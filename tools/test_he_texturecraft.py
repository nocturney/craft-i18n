"""Regression tests for source-locked draft Hebrew TextureCraft catalog."""
import sys
import unittest
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import sync_app
from export_texturecraft import resolved

class HebrewTextureCraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app, cls.parse_errors=sync_app.parse((ROOT/'locales/he/texturecraft.tsv').read_text('utf-8'))
        cls.common, cls.common_errors=sync_app.parse((ROOT/'locales/he/common.tsv').read_text('utf-8'))
        cls.source, cls.source_errors=sync_app.parse((ROOT/'locales/ar/texturecraft.tsv').read_text('utf-8'))

    def test_hebrew_app_catalog_has_139_distinct_source_rows(self):
        self.assertFalse(self.parse_errors)
        self.assertEqual(len(self.app),139)
        self.assertTrue(all(c=='' for c,s in self.app))
        self.assertTrue(all(s and v for (c,s),v in self.app.items()))

    def test_source_parity_and_no_common_retranslations(self):
        self.assertFalse(self.common_errors)
        self.assertFalse(self.source_errors)
        for key,value in self.app.items():
            self.assertIn(key,self.source)
            self.assertNotIn(key,self.common)
            self.assertIsNone(sync_app.text_problem(*key,value))
            self.assertEqual(unicodedata.normalize('NFC',value),value)

    def test_previous_nine_curated_values_preserved(self):
        preserved={
            'Alphas':'תבניות אלפא',
            'Brushed lines':'קווים מוברשים',
            'Flatten layer':'שיטוח שכבה',
            'Displacement (height channel)':'תזוזה (ערוץ גובה)',
            'Add High-Poly Meshes':'הוסף רשתות עתירות מצולעים',
            'Coat normal':'נורמל שכבת הציפוי',
            'Coat roughness':'חספוס שכבת הציפוי',
            'coat rough':'חספוס שכבת הציפוי',
            'Bake mesh maps':'אפיית מפות רשת'
        }
        for source,he in preserved.items():
            self.assertEqual(self.app[('',source)],he)

    def test_hebrew_inheritance_and_real_runtime_labels(self):
        locale=resolved(ROOT,'he-IL')
        self.assertEqual(locale[('','Brush')],'מברשת')
        self.assertEqual(locale[('','Add black mask')],'הוסף מסכה שחורה')
        self.assertEqual(locale[('','Export')],'ייצוא')
        self.assertEqual(locale[('','Fill')],'מילוי')
        self.assertEqual(locale[('','About TextureCraft...')],'אודות TextureCraft...')
        self.assertEqual(len(set(locale)),len(locale))

    def test_quick_wins_resolve_and_preserve_format_placeholders(self):
        locale=resolved(ROOT,'he-IL')
        samples={
            '2D view only':'תצוגת דו־ממד בלבד',
            '3D view only':'תצוגת תלת־ממד בלבד',
            'Add anchor point':'הוספת נקודת עיגון',
            'Add folder':'הוסף תיקייה',
            'Advanced settings':'הגדרות מתקדמות',
            'AO intensity':'עוצמת הסתרה סביבתית',
            'Bake Selected Textures ({n})':'אפיית הטקסטורות שנבחרו ({n})',
            'Baked maps imported: {count}':'יובאו מפות אפויות: {count}',
            '0 turns autosave off. Copies go to {folder}':'0 משבית שמירה אוטומטית. עותקים נשמרים בתיקייה {folder}',
            'Built-in: {mesh}':'מובנה: {mesh}',
        }
        for english,hebrew in samples.items():
            self.assertEqual(locale[('',english)],hebrew,english)
            self.assertIsNone(sync_app.text_problem('',english,hebrew))
        self.assertEqual(len(self.app),139)

if __name__=='__main__':
    unittest.main()
