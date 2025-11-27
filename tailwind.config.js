/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['selector', '[data-mode="dark"]'],
  content: [
    './index.html',
    './src/*.{js,ts,vue}',
    './src/**/*.{js,ts,vue}',
    './src/**/**/*.{js,ts,vue}'
  ],
  theme: {
    fontFamily: {
      sans: ['Helvetica', 'Arial', 'sans-serif']
    },
    extend: {
      colors: {
        blue: {
          DEFAULT: '#193b4d',
          100: '#eaf3f8',
          200: '#bfdbea',
          300: '#94c3dc',
          400: '#69abce',
          500: '#3f93c0',
          600: '#317396',
          700: '#23526b',
          800: '#153140',
          900: '#071015'
        },
        red: {
          DEFAULT: '#E05A47',
          100: '#fbe9e7',
          200: '#f3beb6',
          300: '#eb9286',
          400: '#e26755',
          500: '#da3b25',
          600: '#aa2e1d',
          700: '#792114',
          800: '#49140c',
          900: '#180704'
        }
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            ul: {
              listStyleType: 'disc',
              paddingLeft: '1.25em',
              marginTop: '0.5em',
              marginBottom: '0.5em'
            },
            ol: {
              listStyleType: 'decimal',
              paddingLeft: '1.25em',
              marginTop: '0.5em',
              marginBottom: '0.5em'
            },
            li: {
              marginTop: '0.25em',
              marginBottom: '0.25em'
            },
            p: {
              marginTop: '0.5em',
              marginBottom: '0.5em'
            }
          }
        }
      })
    }
  },
  plugins: []
}
