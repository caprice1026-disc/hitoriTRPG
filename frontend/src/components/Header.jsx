import React from 'react';

const Header = () => {
  return (
    <header>
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/login">Login</a></li>
          <li><a href="/signup">Sign Up</a></li>
          {/* メニューに追加したい内容など。後で修正 */}
        </ul>
      </nav>
    </header>
  );
};

export default Header;