import React from 'react';
import Header from '../components/Header.jsx';
import Footer from '../components/Footer.jsx';

const Home = () => {
  return (
    <div>
      <Header />
      <main>
        {/* ホームページのコンテンツをここに記述 */}
        <h1>Welcome to the adventure</h1>
        <p>ここから冒険を始めましょう。</p>
        <button>Start Game</button>
      </main>
      <Footer />
    </div>
  );
};

export default Home;