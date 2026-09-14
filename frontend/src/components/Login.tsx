import React, { useState } from 'react'
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
  Alert,
  InputAdornment,
  IconButton,
  Chip,
  Divider,
  useTheme,
  alpha,
} from '@mui/material'
import {
  SchoolRounded as SchoolIcon,
  EmailRounded as EmailIcon,
  LockRounded as LockIcon,
  VisibilityRounded as VisibilityIcon,
  VisibilityOffRounded as VisibilityOffIcon,
  FlashOnRounded as QuickLoginIcon,
  Brightness4Rounded as DarkModeIcon,
  Brightness7Rounded as LightModeIcon,
} from '@mui/icons-material'
import { useColorMode } from '@/context/ColorModeContext'

interface LoginProps {
  onLogin: (email: string, password: string) => void
}

export const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const theme = useTheme()
  const { mode, toggleColorMode } = useColorMode()
  const isLight = mode === 'light'

  const [email, setEmail] = useState('principal@eduguard.org')
  const [password, setPassword] = useState('password123')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!email || !password) {
      setError('Please provide an administrative email and password.')
      return
    }

    if (!email.includes('@')) {
      setError('Please enter a valid administrative email address.')
      return
    }

    onLogin(email, password)
  }

  const handleQuickDemoLogin = () => {
    onLogin('principal@eduguard.org', 'password123')
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: isLight
          ? 'radial-gradient(ellipse at top, #e0e7ff 0%, #f8fafc 70%)'
          : 'radial-gradient(ellipse at top, #1e1b4b 0%, #0b0f19 70%)',
        p: 2,
        position: 'relative',
      }}
    >
      {/* Theme Toggle Top Right */}
      <Box sx={{ position: 'absolute', top: 20, right: 24 }}>
        <IconButton onClick={toggleColorMode} color="inherit" sx={{ bgcolor: alpha(theme.palette.text.primary, 0.05) }}>
          {mode === 'dark' ? <LightModeIcon sx={{ color: '#fbbf24' }} /> : <DarkModeIcon sx={{ color: '#6366f1' }} />}
        </IconButton>
      </Box>

      <Container maxWidth="xs">
        <Card
          sx={{
            borderRadius: 4,
            border: `1px solid ${theme.palette.divider}`,
            boxShadow: isLight
              ? '0 20px 40px -15px rgba(79, 70, 229, 0.15)'
              : '0 20px 40px -15px rgba(0, 0, 0, 0.6)',
            overflow: 'hidden',
          }}
        >
          {/* Decorative accent top bar */}
          <Box sx={{ height: 6, background: 'linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%)' }} />

          <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
            <Box sx={{ textAlign: 'center', mb: 3.5 }}>
              <Box
                sx={{
                  width: 54,
                  height: 54,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2,
                  boxShadow: '0 8px 20px rgba(79, 70, 229, 0.3)',
                }}
              >
                <SchoolIcon sx={{ color: '#ffffff', fontSize: 30 }} />
              </Box>
              <Typography variant="h3" sx={{ fontWeight: 800, letterSpacing: '-0.02em', mb: 0.5 }}>
                EduGuard
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Dropout Risk Early Warning & AI Surveillance
              </Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 2.5, borderRadius: 2 }}>
                {error}
              </Alert>
            )}

            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Administrator Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                margin="normal"
                size="medium"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <EmailIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
                    </InputAdornment>
                  ),
                }}
              />

              <TextField
                fullWidth
                label="Security Key / Password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                margin="normal"
                size="medium"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LockIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={() => setShowPassword((p) => !p)} edge="end" size="small">
                        {showPassword ? <VisibilityOffIcon fontSize="small" /> : <VisibilityIcon fontSize="small" />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />

              <Button
                fullWidth
                type="submit"
                variant="contained"
                size="large"
                sx={{
                  mt: 3,
                  mb: 2,
                  py: 1.4,
                  fontSize: '0.95rem',
                  fontWeight: 700,
                  borderRadius: 2.5,
                }}
              >
                Sign In to Platform
              </Button>
            </form>

            <Divider sx={{ my: 2.5 }}>
              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                OR QUICK DEMO
              </Typography>
            </Divider>

            {/* 1-Click Demo Login */}
            <Button
              fullWidth
              variant="outlined"
              onClick={handleQuickDemoLogin}
              startIcon={<QuickLoginIcon sx={{ color: '#f59e0b' }} />}
              sx={{
                py: 1.2,
                borderRadius: 2.5,
                fontWeight: 700,
                borderColor: theme.palette.divider,
                color: 'text.primary',
                '&:hover': {
                  bgcolor: alpha(theme.palette.primary.main, 0.04),
                  borderColor: theme.palette.primary.main,
                },
              }}
            >
              1-Click Demo Login
            </Button>

            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Chip
                label="Sample High School • Connected to Local DB"
                size="small"
                variant="outlined"
                sx={{ fontSize: '0.7rem', color: 'text.secondary' }}
              />
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  )
}
