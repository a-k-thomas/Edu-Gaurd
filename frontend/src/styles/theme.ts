import { createTheme, ThemeOptions } from '@mui/material/styles'

export const getAppTheme = (mode: 'light' | 'dark') => {
  const isLight = mode === 'light'

  const themeOptions: ThemeOptions = {
    palette: {
      mode,
      primary: {
        main: '#4f46e5', // Indigo 600
        light: '#818cf8',
        dark: '#3730a3',
        contrastText: '#ffffff',
      },
      secondary: {
        main: '#06b6d4', // Cyan 500
        light: '#67e8f9',
        dark: '#0e7490',
        contrastText: '#ffffff',
      },
      success: {
        main: '#10b981', // Emerald 500
        light: '#34d399',
        dark: '#059669',
      },
      warning: {
        main: '#f59e0b', // Amber 500
        light: '#fbbf24',
        dark: '#d97706',
      },
      error: {
        main: '#f43f5e', // Rose 500
        light: '#fb7185',
        dark: '#e11d48',
      },
      info: {
        main: '#0284c7', // Sky 600
        light: '#38bdf8',
        dark: '#0369a1',
      },
      background: {
        default: isLight ? '#f8fafc' : '#0b0f19',
        paper: isLight ? '#ffffff' : '#111827',
      },
      text: {
        primary: isLight ? '#0f172a' : '#f8fafc',
        secondary: isLight ? '#64748b' : '#94a3b8',
      },
      divider: isLight ? '#e2e8f0' : 'rgba(255, 255, 255, 0.08)',
    },
    typography: {
      fontFamily: '"Plus Jakarta Sans", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      h1: {
        fontSize: '2.25rem',
        fontWeight: 800,
        letterSpacing: '-0.025em',
        lineHeight: 1.2,
      },
      h2: {
        fontSize: '1.875rem',
        fontWeight: 700,
        letterSpacing: '-0.02em',
        lineHeight: 1.25,
      },
      h3: {
        fontSize: '1.5rem',
        fontWeight: 700,
        letterSpacing: '-0.015em',
        lineHeight: 1.3,
      },
      h4: {
        fontSize: '1.25rem',
        fontWeight: 700,
        letterSpacing: '-0.01em',
        lineHeight: 1.35,
      },
      h5: {
        fontSize: '1.125rem',
        fontWeight: 600,
        lineHeight: 1.4,
      },
      h6: {
        fontSize: '1rem',
        fontWeight: 600,
        lineHeight: 1.5,
      },
      subtitle1: {
        fontSize: '0.9375rem',
        fontWeight: 500,
      },
      subtitle2: {
        fontSize: '0.8125rem',
        fontWeight: 500,
      },
      body1: {
        fontSize: '0.9375rem',
        lineHeight: 1.6,
      },
      body2: {
        fontSize: '0.8125rem',
        lineHeight: 1.5,
      },
      button: {
        fontWeight: 600,
        letterSpacing: '0.01em',
      },
    },
    shape: {
      borderRadius: 12,
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          body: {
            scrollbarColor: isLight ? '#cbd5e1 #f8fafc' : '#334155 #0b0f19',
            '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
              width: 8,
              height: 8,
            },
            '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
              borderRadius: 8,
              backgroundColor: isLight ? '#cbd5e1' : '#334155',
            },
            '&::-webkit-scrollbar-track, & *::-webkit-scrollbar-track': {
              backgroundColor: isLight ? '#f8fafc' : '#0b0f19',
            },
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            borderRadius: 10,
            padding: '8px 18px',
            fontSize: '0.875rem',
            boxShadow: 'none',
            transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
            '&:hover': {
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.25)',
              transform: 'translateY(-1px)',
            },
          },
          containedPrimary: {
            background: 'linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #4338ca 0%, #4f46e5 100%)',
            },
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 16,
            backgroundImage: 'none',
            backgroundColor: isLight ? '#ffffff' : '#111827',
            border: `1px solid ${isLight ? '#e2e8f0' : 'rgba(255, 255, 255, 0.08)'}`,
            boxShadow: isLight
              ? '0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 6px 16px -2px rgba(0, 0, 0, 0.04)'
              : '0 4px 20px 0 rgba(0, 0, 0, 0.35)',
            transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
          },
        },
      },
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: 'none',
            borderRadius: 14,
          },
        },
      },
      MuiTableCell: {
        styleOverrides: {
          root: {
            borderColor: isLight ? '#f1f5f9' : 'rgba(255, 255, 255, 0.06)',
            padding: '14px 18px',
            fontSize: '0.875rem',
          },
          head: {
            fontWeight: 600,
            color: isLight ? '#475569' : '#94a3b8',
            backgroundColor: isLight ? '#f8fafc' : '#161f30',
            textTransform: 'uppercase',
            fontSize: '0.75rem',
            letterSpacing: '0.05em',
          },
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            fontWeight: 600,
            borderRadius: 8,
          },
        },
      },
    },
  }

  return createTheme(themeOptions)
}

export const theme = getAppTheme('light')
