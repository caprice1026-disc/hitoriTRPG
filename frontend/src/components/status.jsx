import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText } from '@material-ui/core';

const StatusDisplay = () => {
  // ステータス情報
  const status = {
    STR: 0,
    DEX: 0,
    INT: 0,
    AGI: 0,
    LUCK: 0,
    HP: 50,
    SAN: 100,
  };

  return (
    // Paperコンポーネントで囲むことで、スタイリングを適用
    // elevation={3}で影をつける
    // padding: '20px'で内側の余白を20pxに設定
    // サイズ感は後で修正。レスポンシブデザインは後で確認。
    <Paper elevation={3} style={{ padding: '20px', maxWidth: '300px' }}>
      <Typography variant="h6" component="h3" style={{ marginBottom: '20px' }}>
        Character Status
      </Typography>
      <List>
        {Object.entries(status).map(([key, value]) => (
          <ListItem key={key}>
            <ListItemText primary={`${key}: ${value}`} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default StatusDisplay;
