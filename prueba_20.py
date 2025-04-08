import ipaddress

def obtener_clase(ip):
    """Determina clase y máscara por defecto [[1]][[6]]"""
    octetos = list(map(int, ip.split('.')))
    if 1 <= octetos[0] <= 126:
        return 'A', '255.0.0.0', 8
    elif 128 <= octetos[0] <= 191:
        return 'B', '255.255.0.0', 16
    elif 192 <= octetos[0] <= 223:
        return 'C', '255.255.255.0', 24
    else:
        return 'Desconocida', '0.0.0.0', 0

def calcular_subredes():
    ip_usuario = input("Ingrese IP con máscara (ej. 10.0.0.0/8): ") or "10.0.0.0/8"
    bits_subred = int(input("Bits para subredes (ej. 2): ") or 2)
    
    # Para procesar entrada
    if '/' in ip_usuario:
        ip_str, mascara_str = ip_usuario.split('/')
        red_original = ipaddress.IPv4Network(f"{ip_str}/{mascara_str}", strict=False)
    else:
        ip_str = ip_usuario
        _, mascara_defecto, _ = obtener_clase(ip_str)
        red_original = ipaddress.IPv4Network(f"{ip_str}/{mascara_defecto}", strict=False)
    
    # Esta parte es para calcular nueva máscara
    nueva_mascara = red_original.prefixlen + bits_subred
    if nueva_mascara > 32:
        print(f"[[3]] Error: Máscara /{nueva_mascara} excede 32 bits")
        return
    
    # Esta parte la uso para generar las subredes
    try:
        subredes = list(red_original.subnets(new_prefix=nueva_mascara))
    except ValueError as e:
        print(f"[[5]] Error en cálculo: {e}")
        return
    
    # Muestra  resultados
    clase, mascara_clase, _ = obtener_clase(str(red_original.network_address))
    print(f"\n--- Red Original: {red_original} ---")
    print(f"Clase: {clase}")
    print(f"Máscara por defecto: {mascara_clase} (/{red_original.prefixlen})")
    print(f"Nueva máscara: {subredes[0].netmask} (/{nueva_mascara})")
    print(f"Subredes creadas: {len(subredes)}")
    print(f"Hosts por subred: {subredes[0].num_addresses - 2}\n")
    
    print("Tabla de subredes:")
    # cabeza de la tabla
    print(f"{'Gerencia':<10} | {'Red':<18} | {'Primera IP':<18} | {'Ultima IP':<18} | {'Broadcast':<18} | {'Gateway':<18} | {'Máscara':<15}")
    
    for idx, subred in enumerate(subredes):
        primer_host = subred.network_address + 1
        broadcast = subred.broadcast_address
        ultimo_host = broadcast - 1
        rango = f"{primer_host} - {ultimo_host}"
        

        gerencia = idx  # comienza en 0
        red = str(subred.network_address)
        primera_ip = str(primer_host)
        ultima_ip = str(ultimo_host)
        broadcast_ip = str(broadcast)
        gateway = str(primer_host)
        mascara = str(subred.netmask)
        
        
        print(f"{gerencia:<10} | {red:<18} | {primera_ip:<18} | {ultima_ip:<18} | {broadcast_ip:<18} | {gateway:<18} | {mascara:<15}")

calcular_subredes()