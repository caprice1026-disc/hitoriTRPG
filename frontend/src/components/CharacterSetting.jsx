import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';

const CharacterSetting = () => {
  const [characterName, setCharacterName] = useState('');
  const [profession, setProfession] = useState('');
  const [stats, setStats] = useState({
    STR: 5,
    DEX: 5,
    INT: 5,
    AGI: 5,
    LUCK: 5
  });

  const handleCharacterNameChange = (event) => {
    setCharacterName(event.target.value);
  };

  const handleProfessionChange = (event) => {
    setProfession(event.target.value);
  };

  const handleUpdateStats = () => {
    // ランダムにステータスを更新する
    setStats({
      STR: Math.floor(Math.random() * 11) + 2,
      DEX: Math.floor(Math.random() * 11) + 2,
      INT: Math.floor(Math.random() * 11) + 2,
      AGI: Math.floor(Math.random() * 11) + 2,
      LUCK: Math.floor(Math.random() * 11) + 2
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const dataToSend = { characterName, profession, stats };
    try {
      const response = await fetch('/api/charactersettings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend)
      });
      const data = await response.json();
      console.log('送信結果:', data);
    } catch (error) {
      console.error('送信エラー:', error);
    }
  };

  return (
    <div>
      <h2>キャラクター設定のフォーム</h2>
      <form onSubmit={handleSubmit}>
        <TextField
          label="キャラクター名"
          value={characterName}
          onChange={handleCharacterNameChange}
          margin="normal"
          fullWidth
        />
        <TextField
          label="職業名"
          value={profession}
          onChange={handleProfessionChange}
          margin="normal"
          fullWidth
        />
        <div>
          <h3>ステータス</h3>
          <p>STR: {stats.STR}, DEX: {stats.DEX}, INT: {stats.INT}, AGI: {stats.AGI}, LUCK: {stats.LUCK}</p>
          <Button onClick={handleUpdateStats} variant="contained" color="secondary">ステータス更新</Button>
        </div>
        <Button type="submit" variant="contained" color="primary">
          送信
        </Button>
      </form>
    </div>
  );
};

export default CharacterSetting;