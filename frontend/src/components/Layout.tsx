import React, { useState } from 'react'
import {
  AppBar,
  Box,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Tooltip,
  Avatar,
  Chip,
  Divider,
  useTheme,
  useMediaQuery,
  Menu,
  MenuItem,
  InputBase,
  alpha,
} from '@mui/material'
import {
  Menu as MenuIcon,
  DashboardRounded as DashboardIcon,
  PeopleAltRounded as PeopleIcon,
  AssessmentRounded as ReportsIcon,
  LogoutRounded as LogoutIcon,
  Brightness4Rounded as DarkModeIcon,
  Brightness7Rounded as LightModeIcon,
  SchoolRounded as SchoolIcon,
  SearchRounded as SearchIcon,
  PsychologyRounded as AiIcon,
  ChevronLeftRounded as ChevronLeftIcon,
  CheckCircleRounded as CheckCircleIcon,
} from '@mui/icons-material'
import { Link, useLocation } from 'react-router-dom'
import { useColorMode } from '@/context/ColorModeContext'

const DRAWER_WIDTH = 260

interface NavbarProps {
  onToggleSidebar: () => void
  onLogout?: () => void
  userEmail?: string
}

export const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar, onLogout, userEmail }) => {
  const theme = useTheme()
  const { mode, toggleColorMode } = useColorMode()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const handleProfileClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        backgroundColor: theme.palette.mode === 'light' ? 'rgba(255, 255, 255, 0.85)' : 'rgba(17, 24, 39, 0.85)',
        backdropFilter: 'blur(12px)',
        borderBottom: `1px solid ${theme.palette.divider}`,
        color: theme.palette.text.primary,
        zIndex: theme.zIndex.drawer + 1,
      }}
    >
      <Toolbar sx={{ minHeight: 64, px: { xs: 2, sm: 3 } }}>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="toggle navigation"
          onClick={onToggleSidebar}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        {/* Brand Icon & Name */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mr: 3 }}>
          <Box
            sx={{
              width: 38,
              height: 38,
              borderRadius: 2.5,
              background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)',
            }}
          >
            <SchoolIcon sx={{ color: '#fff', fontSize: 22 }} />
          </Box>
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: '-0.02em', lineHeight: 1.1 }}>
              EduGuard
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 600, fontSize: '0.7rem' }}>
              Risk Analytics Platform
            </Typography>
          </Box>
        </Box>

        {/* Global Search Bar (Responsive) */}
        {!isMobile && (
          <Box
            sx={{
              position: 'relative',
              borderRadius: 2,
              backgroundColor: theme.palette.mode === 'light' ? alpha(theme.palette.common.black, 0.04) : alpha(theme.palette.common.white, 0.06),
              border: `1px solid ${theme.palette.divider}`,
              display: 'flex',
              alignItems: 'center',
              px: 1.5,
              py: 0.5,
              width: { md: 280, lg: 360 },
              transition: 'all 0.2s ease',
              '&:focus-within': {
                borderColor: theme.palette.primary.main,
                boxShadow: `0 0 0 3px ${alpha(theme.palette.primary.main, 0.15)}`,
              },
            }}
          >
            <SearchIcon sx={{ color: 'text.secondary', fontSize: 20, mr: 1 }} />
            <InputBase
              placeholder="Quick search students, classes, alerts..."
              sx={{ width: '100%', fontSize: '0.85rem' }}
            />
          </Box>
        )}

        <Box sx={{ flexGrow: 1 }} />

        {/* System Status Pill */}
        {!isMobile && (
          <Chip
            icon={<Box className="pulsing-indicator" sx={{ ml: 1 }} />}
            label="AI Engine Online"
            size="small"
            sx={{
              mr: 2,
              fontWeight: 600,
              fontSize: '0.75rem',
              backgroundColor: theme.palette.mode === 'light' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(16, 185, 129, 0.18)',
              color: theme.palette.mode === 'light' ? '#065f46' : '#34d399',
              border: '1px solid rgba(16, 185, 129, 0.25)',
            }}
          />
        )}

        {/* Dark / Light Mode Toggle */}
        <Tooltip title={mode === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}>
          <IconButton onClick={toggleColorMode} color="inherit" sx={{ mr: 1 }}>
            {mode === 'dark' ? <LightModeIcon sx={{ color: '#fbbf24' }} /> : <DarkModeIcon sx={{ color: '#6366f1' }} />}
          </IconButton>
        </Tooltip>

        {/* User Profile Avatar */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton onClick={handleProfileClick} size="small" sx={{ p: 0.5 }}>
            <Avatar
              sx={{
                width: 36,
                height: 36,
                background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                fontSize: '0.9rem',
                fontWeight: 700,
              }}
            >
              {userEmail ? userEmail.charAt(0).toUpperCase() : 'A'}
            </Avatar>
          </IconButton>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            PaperProps={{
              sx: {
                mt: 1.5,
                minWidth: 200,
                borderRadius: 2,
                boxShadow: theme.palette.mode === 'light' ? '0 10px 25px rgba(0,0,0,0.1)' : '0 10px 25px rgba(0,0,0,0.4)',
                border: `1px solid ${theme.palette.divider}`,
              },
            }}
          >
            <Box sx={{ px: 2, py: 1.5 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
                {userEmail || 'Administrator'}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                School Authority • Principal
              </Typography>
            </Box>
            <Divider />
            <MenuItem onClick={() => { handleClose(); onLogout?.() }} sx={{ py: 1.2, color: 'error.main', gap: 1.5 }}>
              <LogoutIcon fontSize="small" />
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                Log Out
              </Typography>
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  )
}

interface SidebarProps {
  open: boolean
  onClose: () => void
  onLogout?: () => void
  userEmail?: string
}

export const Sidebar: React.FC<SidebarProps> = ({ open, onClose, onLogout, userEmail }) => {
  const theme = useTheme()
  const location = useLocation()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const navGroups = [
    {
      group: 'OVERVIEW',
      items: [
        { label: 'Dashboard', icon: DashboardIcon, path: '/dashboard' },
        { label: 'Analytics & Reports', icon: ReportsIcon, path: '/reports' },
      ],
    },
    {
      group: 'STUDENT ROSTER',
      items: [
        { label: 'Students Directory', icon: PeopleIcon, path: '/students' },
      ],
    },
  ]

  const drawerContent = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', py: 2 }}>
      {/* Mobile Header with close button */}
      {isMobile && (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', px: 2, mb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SchoolIcon color="primary" />
            <Typography variant="h6" sx={{ fontWeight: 800 }}>EduGuard</Typography>
          </Box>
          <IconButton onClick={onClose}>
            <ChevronLeftIcon />
          </IconButton>
        </Box>
      )}

      {/* Navigation List */}
      <Box sx={{ flexGrow: 1, px: 2 }}>
        {navGroups.map((group) => (
          <Box key={group.group} sx={{ mb: 2 }}>
            <Typography
              variant="caption"
              sx={{
                px: 1.5,
                mb: 1,
                display: 'block',
                color: 'text.secondary',
                fontWeight: 700,
                fontSize: '0.7rem',
                letterSpacing: '0.08em',
              }}
            >
              {group.group}
            </Typography>
            <List disablePadding>
              {group.items.map((item) => {
                const isActive = location.pathname === item.path || (item.path !== '/dashboard' && location.pathname.startsWith(item.path))
                const IconComponent = item.icon

                return (
                  <ListItemButton
                    key={item.label}
                    component={Link}
                    to={item.path}
                    onClick={() => { if (isMobile) onClose() }}
                    sx={{
                      borderRadius: 2,
                      mb: 0.8,
                      py: 1.2,
                      px: 1.5,
                      backgroundColor: isActive
                        ? theme.palette.mode === 'light' ? 'rgba(79, 70, 229, 0.08)' : 'rgba(99, 102, 241, 0.16)'
                        : 'transparent',
                      color: isActive ? theme.palette.primary.main : theme.palette.text.primary,
                      border: isActive
                        ? `1px solid ${theme.palette.mode === 'light' ? 'rgba(79, 70, 229, 0.2)' : 'rgba(99, 102, 241, 0.3)'}`
                        : '1px solid transparent',
                      transition: 'all 0.18s ease-in-out',
                      '&:hover': {
                        backgroundColor: theme.palette.mode === 'light' ? 'rgba(79, 70, 229, 0.04)' : 'rgba(255, 255, 255, 0.05)',
                        transform: 'translateX(2px)',
                      },
                    }}
                  >
                    <ListItemIcon
                      sx={{
                        minWidth: 36,
                        color: isActive ? theme.palette.primary.main : 'text.secondary',
                      }}
                    >
                      <IconComponent fontSize="small" />
                    </ListItemIcon>
                    <ListItemText
                      primary={item.label}
                      primaryTypographyProps={{
                        fontSize: '0.875rem',
                        fontWeight: isActive ? 700 : 500,
                      }}
                    />
                  </ListItemButton>
                )
              })}
            </List>
          </Box>
        ))}
      </Box>

      {/* AI Model Info Card */}
      <Box sx={{ px: 2, mb: 2 }}>
        <Box
          sx={{
            p: 2,
            borderRadius: 2.5,
            background: theme.palette.mode === 'light'
              ? 'linear-gradient(135deg, rgba(79, 70, 229, 0.06) 0%, rgba(6, 182, 212, 0.06) 100%)'
              : 'linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%)',
            border: `1px solid ${theme.palette.divider}`,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <AiIcon sx={{ color: theme.palette.primary.main, fontSize: 20 }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 700, fontSize: '0.8rem' }}>
              ML Predictor v1.0
            </Typography>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1.2, lineHeight: 1.4 }}>
            Heuristic & gradient-boosted models monitoring 10 risk vectors in real-time.
          </Typography>
          <Chip
            size="small"
            icon={<CheckCircleIcon sx={{ fontSize: '14px !important', color: '#10b981 !important' }} />}
            label="Active Coverage: 100%"
            sx={{
              fontWeight: 600,
              fontSize: '0.68rem',
              backgroundColor: theme.palette.mode === 'light' ? '#fff' : 'rgba(0,0,0,0.2)',
              border: `1px solid ${theme.palette.divider}`,
            }}
          />
        </Box>
      </Box>

      <Divider sx={{ mx: 2, mb: 2 }} />

      {/* User Footer Profile */}
      <Box sx={{ px: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.2, overflow: 'hidden' }}>
          <Avatar
            sx={{
              width: 34,
              height: 34,
              background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
              fontSize: '0.8rem',
              fontWeight: 700,
            }}
          >
            {userEmail ? userEmail.charAt(0).toUpperCase() : 'A'}
          </Avatar>
          <Box sx={{ minWidth: 0 }}>
            <Typography variant="body2" sx={{ fontWeight: 700, textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
              {userEmail ? userEmail.split('@')[0] : 'Admin'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Active Session
            </Typography>
          </Box>
        </Box>
        <Tooltip title="Logout">
          <IconButton size="small" color="inherit" onClick={onLogout}>
            <LogoutIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
    </Box>
  )

  return (
    <Box component="nav" sx={{ width: { md: open ? DRAWER_WIDTH : 0 }, flexShrink: { md: 0 }, transition: 'width 0.25s ease' }}>
      {/* Mobile Drawer */}
      <Drawer
        variant="temporary"
        open={open && isMobile}
        onClose={onClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: DRAWER_WIDTH,
            borderRight: `1px solid ${theme.palette.divider}`,
            backgroundColor: theme.palette.background.paper,
          },
        }}
      >
        {drawerContent}
      </Drawer>

      {/* Desktop Persistent Drawer */}
      <Drawer
        variant="persistent"
        open={open}
        sx={{
          display: { xs: 'none', md: 'block' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: DRAWER_WIDTH,
            borderRight: `1px solid ${theme.palette.divider}`,
            backgroundColor: theme.palette.background.paper,
            top: 64,
            height: 'calc(100% - 64px)',
          },
        }}
      >
        {drawerContent}
      </Drawer>
    </Box>
  )
}
