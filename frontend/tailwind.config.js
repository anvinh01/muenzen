/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        colors: {
          "background": "var(--background)",
            "primary": "var(--primary)",
            "primary-dark": "var(--primary-dark)",
            "secondary": "var(--secondary)",
            "secondary-dark": "var(--secondary-dark)",
            "neutral": "var(--neutral)",
            "white": "var(--white)",
        },
        extend: {
          fontFamily: {
            default: ["Taviraj", "sans-serif"],
          }
        },
        screens: {
          '2xl': {'max': '1535px'},
          // => @media (max-width: 1535px) { ... }
    
          'Desktop': {'max': '1279px'},
          // => @media (max-width: 1279px) { ... }
    
          'laptop': {'max': '1023px'},
          // => @media (max-width: 1023px) { ... }
    
          'tablet': {'max': '767px'},
          // => @media (max-width: 767px) { ... }
    
          'mobile': {'max': '639px'},
          // => @media (max-width: 639px) { ... }
        }
    },
    fontFamily: {

    },
    plugins: [require("@tailwindcss/typography")]
};