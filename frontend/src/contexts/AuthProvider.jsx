import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (email, password) => {
    const response = await axios.post('バックエンドのログインAPIのエンドポイント', {
      email,
      password
    });
    const { token, user } = response.data;
    localStorage.setItem('token', token); // JWTトークンをlocalStorageに保存
    setCurrentUser(user);
  };

  const logout = () => {
    localStorage.removeItem('token'); // localStorageからJWTトークンを削除
    setCurrentUser(null);
  };

  // ページ読み込み時にJWTトークンの検証を行う
  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.post('バックエンドのトークン検証APIのエンドポイント', {
          token
        });
        setCurrentUser(response.data.user); // 検証に成功したらユーザー情報をセット
      }
      setLoading(false);
    };

    verifyToken();
  }, []);

  const value = {
    currentUser,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};