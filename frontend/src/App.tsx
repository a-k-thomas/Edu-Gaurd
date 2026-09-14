import React, { useState, useEffect } from 'react'
import { Box, CssBaseline, ThemeProvider } from '@mui/material'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Login } from '@/components/Login'
import { Navbar, Sidebar } from '@/components/Layout'
import { Dashboard } from '@/components/Dashboard'
import { Students } from '@/components/Students'
import { StudentDetail } from '@/components/StudentDetail'
import { Reports } from '@/components/Reports'
import { ColorModeProvider, useColorMode } from '@/context/ColorModeContext'
import { getAppTheme } from '@/styles/theme'

const AppContent: React.FC = () => {
  const { mode } = useColorMode()
  const theme = React.useMemo(() => getAppTheme(mode), [mode])
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [currentUser, setCurrentUser] = useState<string>('')

  const handleLogin = (email: string, password: string) => {
    if (email && password) {
      setIsAuthenticated(true)
      setCurrentUser(email)
      localStorage.setItem('user', email)
      localStorage.setItem('isAuthenticated', 'true')
    }
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setCurrentUser('')
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
  }

  useEffect(() => {
    const storedAuth = localStorage.getItem('isAuthenticated')
    const storedUser = localStorage.getItem('user')
    if (storedAuth === 'true' && storedUser) {
      setIsAuthenticated(true)
      setCurrentUser(storedUser)
    }
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <Router>
          <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: 'background.default' }}>
            <Navbar
              onToggleSidebar={() => setSidebarOpen((prev) => !prev)}
              onLogout={handleLogout}
              userEmail={currentUser}
            />
            <Box sx={{ display: 'flex', flex: 1, position: 'relative' }}>
              <Sidebar
                open={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                onLogout={handleLogout}
                userEmail={currentUser}
              />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  p: { xs: 2, sm: 3, md: 4 },
                  width: { md: sidebarOpen ? 'calc(100% - 260px)' : '100%' },
                  transition: 'width 0.25s ease, margin 0.25s ease',
                  overflowY: 'auto',
                }}
              >
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/students" element={<Students />} />
                  <Route path="/student/:id" element={<StudentDetail />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="*" element={<Navigate to="/dashboard" />} />
                </Routes>
              </Box>
            </Box>
          </Box>
        </Router>
      )}
    </ThemeProvider>
  )
}

export default function App() {
  return (
    <ColorModeProvider>
      <AppContent />
    </ColorModeProvider>
  )
}
