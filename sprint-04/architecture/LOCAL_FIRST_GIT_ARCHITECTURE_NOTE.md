# GAIA — LOCAL-FIRST GIT ARCHITECTURE NOTE

## OBSERVED MOTIVATION

The current ING_3090 work has highlighted several challenges with the current Git workflow:
- Runtime artifacts and model blobs are being committed to repositories
- Credential exposure risks during development 
- Limited offline capability for 1070 validation
- Need for forensic evidence retention without compromising security
- Inconsistent handling of private vs public data in Git

## BENEFITS

**VERIFIED**
- Improved repository hygiene through proper exclusion of runtime directories
- Better security through isolation of credentials and tokens from version control
- Enhanced offline development capability with local Git server
- Reduced risk of accidental credential commits to remote repositories

**INFERRED**  
- Faster local development cycles without network dependency
- More robust forensic evidence collection with raw data retention
- Better artifact management for large model files
- Improved collaboration workflow through private branches

## RISKS

**VERIFIED**
- Increased complexity in synchronization between local and remote repositories
- Potential for divergent histories if not properly managed
- Risk of data loss if local server fails without proper backup strategy

**INFERRED**
- Learning curve for team members unfamiliar with local-first workflow
- Need for robust secret management solutions
- Potential for confusion during multi-machine development scenarios

## ALTERNATIVES

1. **Traditional Remote-First**: Keep current GitHub-centric workflow (maintains simplicity but has security and offline limitations)
2. **Hybrid Approach**: Local development with selective remote synchronization (compromise between security and collaboration)
3. **Local-First Architecture**: Establish 3090 as primary source of truth with sanitized remote mirror (proposed solution)

## RECOMMENDED ARCHITECTURE

**PROPOSED**
Implement a local-first Git architecture where:
- 3090 serves as the primary Git server/repository for development
- Private branches and experimental work remain local
- Raw forensic evidence is retained locally 
- Sanitization gate ensures only safe content reaches remote repositories
- GitHub becomes a sanitized mirror for collaboration

## SECURITY BOUNDARIES

**VERIFIED**
- Runtime directories properly excluded from Git via .gitignore
- No credentials or tokens in repository history
- Secret scanning implemented to prevent accidental commits

**PROPOSED**
- Local secret management system for development tokens
- Clear classification of artifacts (public/private/raw/sanitized)
- Automated scanning before any remote push operations

## TOKEN CLASSES

**CLASS 0**: No credentials - For read-only testing and documentation work  
**CLASS 1**: Read-only test token - For validation and testing without write access  
**CLASS 2**: Local development token - For local experimentation and development  
**CLASS 3**: Privileged integration token - For integration with external systems (restricted to specific operations)

## SANITIZED MIRROR MODEL

**PROPOSED**
- All content must pass through a sanitization gate before remote synchronization
- Automatic exclusion of:
  * Credentials, tokens, private keys
  * Runtime caches and temporary files  
  * Raw forensic evidence where inappropriate
  * Large model blobs and generated artifacts
- Manual review required for any exceptions to the sanitization rules

## QNAP FUTURE ROLE

**INFERRED**
- **NOW**: Backup storage for critical repository snapshots
- **NEXT**: Git mirror for synchronization between machines  
- **LATER**: Forensic archive for long-term evidence retention
- **NOT YET**: Artifact/model storage (requires further evaluation)

## MIGRATION COMPLEXITY

**INFERRED**
- Moderate complexity due to existing workflows and team familiarity
- Requires updated documentation and training materials
- Need for clear synchronization procedures between local and remote
- Implementation of secret management system

## OPEN QUESTIONS

1. What is the optimal balance between local development freedom and remote collaboration?
2. How should we handle multi-machine development with 1070 hardware?
3. What specific tools are needed for automated sanitization and synchronization?
4. How do we maintain auditability of remote synchronization activities?

## RECOMMENDED NEXT STEP

**VERIFIED**
- Complete the current ING_3090 checkpoint with all documentation
- Establish clear separation between local development and remote mirroring  
- Begin planning for secret management system implementation

**PROPOSED**
- Evaluate local Git server options for 3090 environment
- Implement basic sanitization gate in pre-commit hooks
- Develop training materials for team on local-first workflow

## RELATION TO CURRENT ING_3090 WORK

**VERIFIED**
The current work has demonstrated the need for better repository hygiene and evidence management. The problems encountered during P1→P10 validation, including runtime artifacts being committed to repositories and credential concerns, support the need for a local-first approach.

**INFERRED** 
The architecture would have prevented:
- Accidental commits of ollama-data directories
- Runtime artifact pollution in repository history  
- Security risks from potential credential exposure

This local-first approach would provide better foundation for forensic evidence collection while maintaining security boundaries between development and production environments.