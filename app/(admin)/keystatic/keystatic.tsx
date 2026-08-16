'use client'

// The Keystatic admin app. `makePage` builds the full CMS UI from the config.
// Must be a Client Component ('use client') because the editor runs in the browser.
import { makePage } from '@keystatic/next/ui/app'
import config from '@/keystatic.config'

export default makePage(config)
