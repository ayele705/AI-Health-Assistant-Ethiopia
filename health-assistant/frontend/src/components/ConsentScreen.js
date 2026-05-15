import React, { useState, useEffect } from 'react';

const SCRIPTS = {
  en: {
    title: 'Before We Begin',
    text: 'This assistant will ask about your symptoms to give health guidance. We collect only: symptoms, age range, sex, and language. We do NOT collect your name or phone number. You can stop and delete your data at any time.',
    agree: 'I Agree — Start',
    caregiver: 'I am answering for someone else (Caregiver Mode)',
    withdraw: 'No, Cancel',
    disclaimer: '️ This is not a clinical diagnosis. Always consult a qualified health worker.',
  },
  am: {
    title: 'ከመጀመራችን በፊት',
    text: 'ይህ ረዳት ምልክቶችዎን ይጠይቃል። የምንሰበስበው ምልክቶች፣ የዕድሜ ክልል፣ ጾታ እና ቋንቋ ብቻ ነው። ስምዎን ወይም ስልክ ቁጥርዎን አንሰበስብም።',
    agree: 'እሺ — ጀምር',
    caregiver: 'ለሌላ ሰው ምላሽ እሰጣለሁ (ተንከባካቢ ሁነታ)',
    withdraw: 'አይ፣ ሰርዝ',
    disclaimer: '️ ይህ ክሊኒካዊ ምርመራ አይደለም። ሁልጊዜ ለህክምና ውሳኔ ብቁ የጤና ሠራተኛ ያማክሩ።',
  },
  om: {
    title: 'Jalqabuun Dura',
    text: 'Gargaaraan kun mallattoolee keessan gaafata. Odeeffannoo walitti qabnu: mallattoolee, umurii, saala fi afaan qofa.',
    agree: 'Eyyee — Jalqabi',
    caregiver: 'Nama biraa bakka bu\'uun deebii kennaa jira',
    withdraw: 'Lakki, Dhaabi',
    disclaimer: '️ Kun dhukkuba adda baasuu miti. Ogeessa fayyaa mariisi.',
  },
  ti: {
    title: 'ቅድሚ ምጅማርና',
    text: 'እዚ ሓጋዚ ምልክታትካ ክሓትት እዩ። ዝእክቦ ሓበሬታ ምልክታት፣ ዕድሜ፣ ጾታን ቋንቋን ጥራይ እዩ።',
    agree: 'እወ — ጀምር',
    caregiver: 'ንካልእ ሰብ ትምልስ ኣለኻ',
    withdraw: 'ኣይፋል፣ ሰርዝ',
    disclaimer: '️ እዚ ክሊኒካዊ ምርመራ ኣይኮነን። ሓኪም ተወከስ።',
  },
  sid: {
    title: 'Jalqabuun Dura',
    text: 'Gargaaraan kun mallattoolee keessan gaafata. Odeeffannoo qofa walitti qabna.',
    agree: 'Eyyee — Jalqabi',
    caregiver: 'Nama biraa bakka bu\'uun deebii kennaa jira',
    withdraw: 'Lakki, Dhaabi',
    disclaimer: '️ Kun dhukkuba adda baasuu miti. Ogeessa fayyaa mariisi.',
  },
  so: {
    title: 'Intaan Bilowno',
    text: 'Kaaliyahan ayaa su\'aalo kaa weydiin doona calaamadahaaga si uu u bixiyo hagitaanka caafimaadka. Waxaan uruurinaa oo keliya: calaamadaha, xadka da\'da, jinsiga, iyo luqadda. Magacaaga ama lambarka telefoonkaaga kuma uruurinno.',
    agree: 'Waan Ogolahay — Bilow',
    caregiver: 'Waxaan u jawaabayaa qof kale (Qaabka Daryeelaha)',
    withdraw: 'Maya, Jooji',
    disclaimer: '️ Kani ma aha ogaanshaha caafimaadka. Had iyo jeer la tasho shaqaale caafimaad.',
  },
  aa: {
    title: 'Intaan Bilowno',
    text: 'Kaaliyahan ayaa su\'aalo kaa weydiin doona calaamadahaaga si uu u bixiyo hagitaanka caafimaadka. Waxaan uruurinaa oo keliya: calaamadaha, xadka da\'da, jinsiga, iyo luqadda.',
    agree: 'Waan Ogolahay — Bilow',
    caregiver: 'Waxaan u jawaabayaa qof kale',
    withdraw: 'Maya, Jooji',
    disclaimer: '️ Kani ma aha ogaanshaha caafimaadka. La tasho shaqaale caafimaad.',
  },
  wal: {
    title: 'Jalqabuun Dura',
    text: 'Gargaaraan kun mallattoolee keessan gaafata. Odeeffannoo qofa walitti qabna.',
    agree: 'Eyyee — Jalqabi',
    caregiver: 'Nama biraa bakka bu\'uun deebii kennaa jira',
    withdraw: 'Lakki, Dhaabi',
    disclaimer: '️ Kun dhukkuba adda baasuu miti. Ogeessa fayyaa mariisi.',
  },
  had: {
    title: 'Jalqabuun Dura',
    text: 'Gargaaraan kun mallattoolee keessan gaafata. Odeeffannoo qofa walitti qabna.',
    agree: 'Eyyee — Jalqabi',
    caregiver: 'Nama biraa bakka bu\'uun deebii kennaa jira',
    withdraw: 'Lakki, Dhaabi',
    disclaimer: '️ Kun dhukkuba adda baasuu miti. Ogeessa fayyaa mariisi.',
  },
};

export default function ConsentScreen({ lang, onAgree, onCaregiver, onWithdraw }) {
  const s = SCRIPTS[lang] || SCRIPTS['en'];

  return (
    <div className="consent-screen" role="dialog" aria-modal="true" aria-labelledby="consent-title">
      <h2 id="consent-title" className="consent-title">{s.title}</h2>
      <p className="consent-text">{s.text}</p>
      <p className="consent-disclaimer">{s.disclaimer}</p>

      <div className="consent-actions">
        <button className="consent-btn agree" onClick={onAgree} aria-label={s.agree}>
           {s.agree}
        </button>
        <button className="consent-btn caregiver" onClick={onCaregiver} aria-label={s.caregiver}>
           {s.caregiver}
        </button>
        <button className="consent-btn withdraw" onClick={onWithdraw} aria-label={s.withdraw}>
           {s.withdraw}
        </button>
      </div>
    </div>
  );
}
